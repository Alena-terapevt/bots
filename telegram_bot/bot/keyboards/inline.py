"""Inline-клавиатуры для бота"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu() -> InlineKeyboardMarkup:
    """Главное меню"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="📚 Все материалы", callback_data="materials"))
    builder.row(InlineKeyboardButton(text="🆘 У меня проблема", callback_data="problems"))
    builder.row(InlineKeyboardButton(text="💰 Оформить доступ", callback_data="subscribe"))
    builder.row(InlineKeyboardButton(text="💬 Связаться с автором", callback_data="contacts"))
    builder.row(InlineKeyboardButton(text="📅 Записаться на встречу", callback_data="booking"))
    builder.row(InlineKeyboardButton(text="⭐ Отзывы и кейсы", callback_data="reviews"))
    builder.row(InlineKeyboardButton(text="❓ Помощь", callback_data="help"))
    
    return builder.as_markup()


def get_back_to_menu() -> InlineKeyboardMarkup:
    """Кнопка "Назад в меню" """
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu"))
    return builder.as_markup()


def get_materials_menu() -> InlineKeyboardMarkup:
    """Меню раздела материалов"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🎥 По формату", callback_data="materials_format"))
    builder.row(InlineKeyboardButton(text="📂 По темам", callback_data="materials_theme"))
    builder.row(InlineKeyboardButton(text="🔥 Популярное", callback_data="materials_popular"))
    builder.row(InlineKeyboardButton(text="🔍 Поиск", callback_data="materials_search"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu"))
    
    return builder.as_markup()


def get_formats_menu() -> InlineKeyboardMarkup:
    """Меню форматов материалов"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🎥 Видео", callback_data="format_video"))
    builder.row(InlineKeyboardButton(text="📄 Статьи", callback_data="format_article"))
    builder.row(InlineKeyboardButton(text="🎧 Аудио", callback_data="format_audio"))
    builder.row(InlineKeyboardButton(text="📋 Конспекты", callback_data="format_pdf"))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="materials"))
    
    return builder.as_markup()


def get_problems_menu() -> InlineKeyboardMarkup:
    """Меню категорий проблем"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🧘 Проблемы со спиной", callback_data="problem_back"))
    builder.row(InlineKeyboardButton(text="🤕 Головные боли", callback_data="problem_head"))
    builder.row(InlineKeyboardButton(text="😴 Упадок сил", callback_data="problem_fatigue"))
    builder.row(InlineKeyboardButton(text="🦵 Проблемы с ногами", callback_data="problem_legs"))
    builder.row(InlineKeyboardButton(text="😰 Стресс и тревожность", callback_data="problem_stress"))
    builder.row(InlineKeyboardButton(text="💤 Проблемы со сном", callback_data="problem_sleep"))
    builder.row(InlineKeyboardButton(text="❓ Другое", callback_data="problem_other"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu"))
    
    return builder.as_markup()


def get_material_keyboard(material_id: int, has_access: bool = False) -> InlineKeyboardMarkup:
    """Клавиатура для конкретного материала"""
    builder = InlineKeyboardBuilder()
    
    if has_access:
        builder.row(InlineKeyboardButton(text="📥 Получить материал", callback_data=f"get_material_{material_id}"))
    else:
        builder.row(InlineKeyboardButton(text="💰 Оформить доступ", callback_data="subscribe"))
    
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data="materials"))
    
    return builder.as_markup()


def get_subscription_keyboard(price: int) -> InlineKeyboardMarkup:
    """Клавиатура для оформления подписки"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text=f"💳 Оплатить {price}₽", callback_data="pay"))
    builder.row(InlineKeyboardButton(text="ℹ️ Подробнее о подписке", callback_data="subscribe_info"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu"))
    
    return builder.as_markup()


def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для оплаты"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment_confirm"))
    builder.row(InlineKeyboardButton(text="❌ Отменить", callback_data="menu"))
    
    return builder.as_markup()


def get_consultation_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура после запроса консультации"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="💬 Написать сейчас", callback_data="contacts"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu"))
    
    return builder.as_markup()


def get_booking_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для записи на встречу"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="📝 Оставить контакты", callback_data="booking_form"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu"))
    
    return builder.as_markup()


def get_reviews_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для отзывов"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="✍️ Оставить отзыв", callback_data="leave_review"))
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="menu"))
    
    return builder.as_markup()


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Админская клавиатура"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"))
    builder.row(InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users"))
    builder.row(InlineKeyboardButton(text="📤 Рассылка", callback_data="admin_broadcast"))
    
    return builder.as_markup()
