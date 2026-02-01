"""Handler для всех Labs и практик"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import (
    get_recovery_reset_menu, get_breath_lab_menu, get_body_lab_menu,
    get_core_lab_menu, get_mind_lab_menu, get_practices_list, get_back_button
)
from bot.utils.texts import (
    RECOVERY_RESET_TEXT, RECOVERY_DAY_TEXT, BREATH_LAB_TEXT,
    BODY_LAB_TEXT, CORE_LAB_TEXT, MIND_LAB_TEXT,
    PRACTICE_PLACEHOLDER, PRACTICE_SENT
)
from bot.database.sheets import sheets_manager
from config.config import Config

logger = logging.getLogger(__name__)

router = Router()
config = Config()

# ID закрытого канала с материалами
MATERIALS_CHANNEL_ID = -1003702761962


# ============= RECOVERY RESET =============

@router.callback_query(F.data == "lab_recovery")
async def show_recovery_reset(callback: CallbackQuery):
    """Показать Recovery Reset"""
    
    await callback.message.edit_text(
        RECOVERY_RESET_TEXT,
        reply_markup=get_recovery_reset_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("recovery_day"))
async def show_recovery_day(callback: CallbackQuery):
    """Показать конкретный день Recovery Reset"""
    
    day_num = callback.data.split('day')[1]
    
    # Описания дней
    day_descriptions = {
        '1': 'Знакомство с телом и дыханием',
        '2': 'Углубление практики',
        '3': 'Интеграция и закрепление'
    }
    
    text = RECOVERY_DAY_TEXT.format(
        day=day_num,
        description=day_descriptions.get(day_num, '')
    )
    
    # Пока нет практик - заглушка
    text += "\n<i>Практики добавляются...</i>"
    
    # В будущем здесь будет список практик для дня
    # practices = get_practices_for_day(day_num)
    # keyboard = get_practices_list(practices, f"recovery_day{day_num}")
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_button("lab_recovery", "🔙 К списку дней")
    )
    
    await callback.answer()


# ============= BREATH LAB =============

@router.callback_query(F.data == "lab_breath")
async def show_breath_lab(callback: CallbackQuery):
    """Показать Breath Lab"""
    
    await callback.message.edit_text(
        BREATH_LAB_TEXT,
        reply_markup=get_breath_lab_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("breath_"))
async def show_breath_category(callback: CallbackQuery):
    """Показать категорию дыхательных практик"""
    
    category = callback.data.split('_')[1]
    
    category_names = {
        'recovery': '🌊 Восстановительное дыхание',
        'balance': '⚖️ Балансирующее дыхание',
        'activating': '⚡ Активирующее дыхание',
        'body': '💫 Дыхание с телом'
    }
    
    title = category_names.get(category, 'Дыхательные практики')
    
    text = f"<b>{title}</b>\n\n<i>Практики добавляются...</i>"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_button("lab_breath")
    )
    
    await callback.answer()


# ============= BODY LAB =============

@router.callback_query(F.data == "lab_body")
async def show_body_lab(callback: CallbackQuery):
    """Показать Body Lab"""
    
    await callback.message.edit_text(
        BODY_LAB_TEXT,
        reply_markup=get_body_lab_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("body_"))
async def show_body_category(callback: CallbackQuery):
    """Показать категорию практик для тела"""
    
    category = callback.data.split('_')[1]
    
    category_names = {
        'diaphragm': '🫁 Диафрагма и рёбра',
        'belly': '🤰 Живот',
        'pelvic': '🌸 Тазовое дно',
        'mobility': '🌊 Мягкая мобилизация',
        'joints': '🦴 Суставная подвижность',
        'whole': '✨ Всё тело'
    }
    
    title = category_names.get(category, 'Практики для тела')
    
    text = f"<b>{title}</b>\n\n<i>Практики добавляются...</i>"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_button("lab_body")
    )
    
    await callback.answer()


# ============= CORE LAB =============

@router.callback_query(F.data == "lab_core")
async def show_core_lab(callback: CallbackQuery):
    """Показать Core Lab"""
    
    await callback.message.edit_text(
        CORE_LAB_TEXT,
        reply_markup=get_core_lab_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("core_"))
async def show_core_category(callback: CallbackQuery):
    """Показать категорию практик Core Lab"""
    
    category = callback.data.split('_')[1]
    
    category_names = {
        'neck': '🦒 Шея и голова',
        'thoracic': '🫀 Грудной отдел',
        'lumbar': '🌀 Поясница',
        'center': '⚓ Центр и опора',
        'joints': '🦴 Суставы',
        'integrity': '🌟 Целостность тела'
    }
    
    title = category_names.get(category, 'Практики Core Lab')
    
    text = f"<b>{title}</b>\n\n<i>Практики добавляются...</i>"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_button("lab_core")
    )
    
    await callback.answer()


# ============= MIND LAB =============

@router.callback_query(F.data == "lab_mind")
async def show_mind_lab(callback: CallbackQuery):
    """Показать Mind Lab"""
    
    await callback.message.edit_text(
        MIND_LAB_TEXT,
        reply_markup=get_mind_lab_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("mind_"))
async def show_mind_category(callback: CallbackQuery):
    """Показать категорию практик Mind Lab"""
    
    category = callback.data.split('_')[1]
    
    category_names = {
        'relaxation': '🌙 Расслабление',
        'meditation': '🧘‍♀️ Медитации',
        'state': '🌈 Работа с состоянием',
        'attention': '🎯 Возвращение внимания'
    }
    
    title = category_names.get(category, 'Практики Mind Lab')
    
    text = f"<b>{title}</b>\n\n<i>Практики добавляются...</i>"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_button("lab_mind")
    )
    
    await callback.answer()


# ============= ПРАКТИКИ =============

@router.callback_query(F.data.startswith("practice_"))
async def get_practice(callback: CallbackQuery):
    """Получить конкретную практику"""
    
    practice_id = int(callback.data.split('_')[1])
    user_id = callback.from_user.id
    
    # Проверяем доступ
    has_access = sheets_manager.check_payment_status(user_id)
    
    if not has_access:
        await callback.answer("🔒 Требуется подписка", show_alert=True)
        return
    
    # Здесь будет отправка реального контента из канала
    # Пока заглушка
    
    await callback.message.answer(
        PRACTICE_PLACEHOLDER,
        reply_markup=get_back_button("menu")
    )
    
    await callback.answer("✅ Практика")
