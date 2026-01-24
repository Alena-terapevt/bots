"""Handler для раздела материалов"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import (
    get_materials_menu, get_formats_menu, get_back_to_menu,
    get_material_keyboard, get_subscription_keyboard
)
from bot.utils.texts import (
    MATERIALS_INTRO, MATERIAL_LOCKED, SUBSCRIPTION_OFFER
)
from bot.database.sheets import sheets_manager
from config.config import Config

logger = logging.getLogger(__name__)

router = Router()
config = Config()


# ID закрытого канала с материалами
MATERIALS_CHANNEL_ID = -1003702761962

# Placeholder материалы (потом заменишь на реальные из БД)
SAMPLE_MATERIALS = {
    'video': [
        {
            'id': 1,
            'title': 'Базовая практика для спины',
            'description': 'Упражнения для расслабления мышц спины и улучшения осанки (15 минут)',
            'message_id': 2,  # ID сообщения в канале
            'category': 'back'
        },
        # Добавь сюда больше видео по мере загрузки
        # {
        #     'id': 2,
        #     'title': 'Утренняя энергия',
        #     'description': 'Комплекс упражнений для бодрого начала дня (10 минут)',
        #     'message_id': 3,
        #     'category': 'fatigue'
        # }
    ],
    'article': [
        # {
        #     'id': 3,
        #     'title': '10 правил здоровой спины',
        #     'description': 'Статья о том, как сохранить здоровье позвоночника',
        #     'message_id': 4,  # ID сообщения с текстом в канале
        #     'category': 'back'
        # }
    ],
    'audio': [
        # {
        #     'id': 4,
        #     'title': 'Медитация для сна',
        #     'description': 'Расслабляющая медитация перед сном (20 минут)',
        #     'message_id': 5,
        #     'category': 'sleep'
        # }
    ]
}


@router.callback_query(F.data == "materials")
async def show_materials(callback: CallbackQuery, requires_subscription: bool = False):
    """Показать раздел материалов"""
    
    await callback.message.edit_text(
        MATERIALS_INTRO,
        reply_markup=get_materials_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data == "materials_format")
async def show_formats(callback: CallbackQuery):
    """Показать форматы материалов"""
    
    text = "🎥 <b>Выберите формат материалов:</b>"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_formats_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("format_"))
async def show_materials_by_format(callback: CallbackQuery, requires_subscription: bool = False):
    """Показать материалы выбранного формата"""
    
    format_type = callback.data.split('_')[1]
    user_id = callback.from_user.id
    
    # Проверяем подписку
    has_access = sheets_manager.check_payment_status(user_id)
    
    if not has_access and requires_subscription:
        # Показываем предложение оформить подписку
        await callback.message.edit_text(
            SUBSCRIPTION_OFFER.format(price=config.SUBSCRIPTION_PRICE),
            reply_markup=get_subscription_keyboard(config.SUBSCRIPTION_PRICE)
        )
        await callback.answer("🔒 Требуется подписка")
        return
    
    # Получаем материалы выбранного формата
    materials = SAMPLE_MATERIALS.get(format_type, [])
    
    if not materials:
        await callback.message.edit_text(
            "Материалы этого формата скоро появятся! 🎬",
            reply_markup=get_back_to_menu()
        )
        await callback.answer()
        return
    
    # Формируем список материалов
    text = f"<b>📚 Материалы ({format_type}):</b>\n\n"
    
    for mat in materials[:5]:  # Показываем первые 5
        emoji = "🎥" if format_type == "video" else "📄" if format_type == "article" else "🎧"
        text += f"{emoji} <b>{mat['title']}</b>\n"
        text += f"<i>{mat['description']}</i>\n\n"
    
    if has_access:
        text += "✅ У вас есть доступ ко всем материалам!"
    else:
        text += "🔒 Для доступа нужна подписка"
    
    await callback.message.edit_text(
        text,
        reply_markup=get_material_keyboard(1, has_access)
    )
    
    await callback.answer()


@router.callback_query(F.data == "materials_theme")
async def show_themes(callback: CallbackQuery):
    """Показать темы материалов"""
    
    text = """
📂 <b>Материалы по темам:</b>

🧘 Позвоночник и осанка
🌬 Дыхательные практики
⚡ Работа с энергией
😌 Снятие напряжения
💪 Укрепление тела

<i>Выберите тему в разделе "У меня проблема"</i>
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data == "materials_popular")
async def show_popular(callback: CallbackQuery, requires_subscription: bool = False):
    """Показать популярные материалы"""
    
    user_id = callback.from_user.id
    has_access = sheets_manager.check_payment_status(user_id)
    
    if not has_access and requires_subscription:
        await callback.message.edit_text(
            SUBSCRIPTION_OFFER.format(price=config.SUBSCRIPTION_PRICE),
            reply_markup=get_subscription_keyboard(config.SUBSCRIPTION_PRICE)
        )
        await callback.answer("🔒 Требуется подписка")
        return
    
    text = """
🔥 <b>Популярные материалы:</b>

1. 🎥 Базовая практика для спины (500+ просмотров)
2. 🎥 Утренняя энергия (450+ просмотров)
3. 🎧 Медитация для сна (400+ просмотров)
4. 📄 10 правил здоровой спины (380+ просмотров)
5. 🎥 Дыхание для расслабления (350+ просмотров)

<i>Скоро здесь появятся реальные материалы!</i>
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data == "materials_search")
async def show_search(callback: CallbackQuery):
    """Поиск материалов"""
    
    text = """
🔍 <b>Поиск материалов</b>

Напишите ключевое слово для поиска материалов.

Например: <i>спина, усталость, сон, энергия</i>

<i>Функция поиска будет добавлена в следующей версии!</i>
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data.startswith("get_material_"))
async def get_material(callback: CallbackQuery):
    """Получить конкретный материал"""
    
    material_id = int(callback.data.split('_')[2])
    user_id = callback.from_user.id
    
    # Проверяем доступ
    has_access = sheets_manager.check_payment_status(user_id)
    
    if not has_access:
        await callback.answer("🔒 Требуется подписка", show_alert=True)
        return
    
    # Ищем материал по ID
    material = None
    for format_type, materials_list in SAMPLE_MATERIALS.items():
        for mat in materials_list:
            if mat['id'] == material_id:
                material = mat
                break
        if material:
            break
    
    if not material:
        await callback.answer("Материал не найден", show_alert=True)
        return
    
    # Увеличиваем счетчик просмотров
    sheets_manager.increment_counter(user_id, 'materials_viewed')
    
    try:
        # Пересылаем сообщение из канала пользователю
        await callback.bot.forward_message(
            chat_id=user_id,
            from_chat_id=MATERIALS_CHANNEL_ID,
            message_id=material['message_id']
        )
        
        await callback.answer("✅ Материал отправлен!")
        
        # Отправляем подтверждение
        await callback.message.answer(
            f"📥 <b>{material['title']}</b>\n\n"
            f"<i>{material['description']}</i>\n\n"
            "Материал отправлен выше ⬆️"
        )
        
    except Exception as e:
        logger.error(f"Failed to forward material: {e}")
        await callback.answer("❌ Ошибка при отправке материала", show_alert=True)
        await callback.message.answer(
            "❌ <b>Не удалось отправить материал</b>\n\n"
            "Возможные причины:\n"
            "• Бот не является администратором канала\n"
            "• Неверный ID сообщения\n\n"
            "Обратитесь к администратору."
        )
