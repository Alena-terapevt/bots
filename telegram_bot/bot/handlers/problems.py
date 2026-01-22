"""Handler для раздела "У меня проблема" """

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.keyboards.inline import (
    get_problems_menu, get_back_to_menu, get_consultation_keyboard
)
from bot.utils.texts import (
    PROBLEMS_INTRO, PROBLEMS, PROBLEM_MATERIALS,
    NO_MATERIALS_FOUND, CONSULTATION_REQUEST_SENT
)
from bot.database.sheets import sheets_manager
from config.config import Config

logger = logging.getLogger(__name__)

router = Router()
config = Config()


class ConsultationStates(StatesGroup):
    """Состояния для запроса консультации"""
    waiting_for_description = State()


@router.callback_query(F.data == "problems")
async def show_problems(callback: CallbackQuery):
    """Показать категории проблем"""
    
    await callback.message.edit_text(
        PROBLEMS_INTRO,
        reply_markup=get_problems_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("problem_"))
async def show_problem_materials(callback: CallbackQuery, state: FSMContext):
    """Показать материалы для выбранной проблемы"""
    
    problem_key = callback.data.split('_')[1]
    user_id = callback.from_user.id
    
    # Обрабатываем "Другое"
    if problem_key == "other":
        await callback.message.edit_text(
            "💬 <b>Опишите вашу проблему</b>\n\n"
            "Напишите подробно, что вас беспокоит, и я передам ваш запрос Алёне.\n\n"
            "<i>Алёна ответит вам в течение 24 часов.</i>",
            reply_markup=get_back_to_menu()
        )
        
        # Переходим в состояние ожидания описания
        await state.set_state(ConsultationStates.waiting_for_description)
        await callback.answer()
        return
    
    # Получаем информацию о проблеме
    problem_info = PROBLEMS.get(problem_key, {})
    
    if not problem_info:
        await callback.answer("Проблема не найдена", show_alert=True)
        return
    
    # Сохраняем проблему в Google Sheets
    sheets_manager.add_problem(user_id, problem_info['title'])
    
    # Формируем список материалов (placeholder)
    text = PROBLEM_MATERIALS.format(problem_title=problem_info['title'])
    text += "\n"
    text += "1. 🎥 <b>Видео-практика</b> - 15 минут\n"
    text += "   <i>Упражнения для решения проблемы</i>\n\n"
    text += "2. 📄 <b>Статья</b>\n"
    text += "   <i>Подробное руководство</i>\n\n"
    text += "3. 🎧 <b>Аудио-медитация</b> - 20 минут\n"
    text += "   <i>Расслабляющая практика</i>\n\n"
    text += "<i>💡 Реальные материалы будут добавлены после загрузки контента</i>\n\n"
    text += "Не нашли подходящее решение? Напишите Алёне напрямую! 👇"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_consultation_keyboard()
    )
    
    await callback.answer()


@router.message(ConsultationStates.waiting_for_description)
async def process_consultation_request(message: Message, state: FSMContext):
    """Обработка запроса на консультацию"""
    
    user = message.from_user
    description = message.text
    
    # Сохраняем запрос в Google Sheets
    sheets_manager.increment_counter(user.id, 'consultation_requests')
    
    # Отправляем уведомление админу
    admin_text = f"""
🔔 <b>Новый запрос на консультацию</b>

<b>От:</b> {user.first_name} {user.last_name or ''} (@{user.username or 'нет username'})
<b>ID:</b> <code>{user.id}</code>

<b>Проблема:</b>
{description}

<b>Дата:</b> {message.date.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    try:
        from aiogram import Bot
        bot = message.bot
        await bot.send_message(config.ADMIN_ID, admin_text)
        logger.info(f"Consultation request sent to admin from user {user.id}")
    except Exception as e:
        logger.error(f"Failed to send consultation request to admin: {e}")
    
    # Отправляем подтверждение пользователю
    await message.answer(
        CONSULTATION_REQUEST_SENT,
        reply_markup=get_back_to_menu()
    )
    
    # Сбрасываем состояние
    await state.clear()
