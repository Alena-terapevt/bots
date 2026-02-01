"""Inline-клавиатуры для бота Recovery Lab"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu() -> InlineKeyboardMarkup:
    """Главное меню - 6 Labs + Информация"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🔄 Recovery Reset", callback_data="lab_recovery"))
    builder.row(InlineKeyboardButton(text="🌬 Breath Lab", callback_data="lab_breath"))
    builder.row(InlineKeyboardButton(text="💆 Body Lab", callback_data="lab_body"))
    builder.row(InlineKeyboardButton(text="🧘 Core Lab", callback_data="lab_core"))
    builder.row(InlineKeyboardButton(text="🧠 Mind Lab", callback_data="lab_mind"))
    builder.row(InlineKeyboardButton(text="ℹ️ Информация", callback_data="info"))
    builder.row(InlineKeyboardButton(text="💰 Оформить подписку", callback_data="subscribe"))
    
    return builder.as_markup()


def get_back_button(callback_data: str, text: str = "🔙 Назад") -> InlineKeyboardMarkup:
    """Универсальная кнопка Назад"""
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=text, callback_data=callback_data))
    return builder.as_markup()


def get_recovery_reset_menu() -> InlineKeyboardMarkup:
    """Меню Recovery Reset - 3 дня"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="📅 День 1", callback_data="recovery_day1"))
    builder.row(InlineKeyboardButton(text="📅 День 2", callback_data="recovery_day2"))
    builder.row(InlineKeyboardButton(text="📅 День 3", callback_data="recovery_day3"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    
    return builder.as_markup()


def get_breath_lab_menu() -> InlineKeyboardMarkup:
    """Меню Breath Lab"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🌊 Восстановительное дыхание", callback_data="breath_recovery"))
    builder.row(InlineKeyboardButton(text="⚖️ Балансирующее дыхание", callback_data="breath_balance"))
    builder.row(InlineKeyboardButton(text="⚡ Активирующее дыхание", callback_data="breath_activating"))
    builder.row(InlineKeyboardButton(text="💫 Дыхание с телом", callback_data="breath_body"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    
    return builder.as_markup()


def get_body_lab_menu() -> InlineKeyboardMarkup:
    """Меню Body Lab"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🫁 Диафрагма и рёбра", callback_data="body_diaphragm"))
    builder.row(InlineKeyboardButton(text="🤰 Живот", callback_data="body_belly"))
    builder.row(InlineKeyboardButton(text="🌸 Тазовое дно", callback_data="body_pelvic"))
    builder.row(InlineKeyboardButton(text="🌊 Мягкая мобилизация", callback_data="body_mobility"))
    builder.row(InlineKeyboardButton(text="🦴 Суставная подвижность", callback_data="body_joints"))
    builder.row(InlineKeyboardButton(text="✨ Всё тело", callback_data="body_whole"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    
    return builder.as_markup()


def get_core_lab_menu() -> InlineKeyboardMarkup:
    """Меню Core Lab"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🦒 Шея и голова", callback_data="core_neck"))
    builder.row(InlineKeyboardButton(text="🫀 Грудной отдел", callback_data="core_thoracic"))
    builder.row(InlineKeyboardButton(text="🌀 Поясница", callback_data="core_lumbar"))
    builder.row(InlineKeyboardButton(text="⚓ Центр и опора", callback_data="core_center"))
    builder.row(InlineKeyboardButton(text="🦴 Суставы", callback_data="core_joints"))
    builder.row(InlineKeyboardButton(text="🌟 Целостность тела", callback_data="core_integrity"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    
    return builder.as_markup()


def get_mind_lab_menu() -> InlineKeyboardMarkup:
    """Меню Mind Lab"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="🌙 Расслабление", callback_data="mind_relaxation"))
    builder.row(InlineKeyboardButton(text="🧘‍♀️ Медитации", callback_data="mind_meditation"))
    builder.row(InlineKeyboardButton(text="🌈 Работа с состоянием", callback_data="mind_state"))
    builder.row(InlineKeyboardButton(text="🎯 Возвращение внимания", callback_data="mind_attention"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    
    return builder.as_markup()


def get_info_menu() -> InlineKeyboardMarkup:
    """Меню Информация"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="📖 О проекте", callback_data="info_about"))
    builder.row(InlineKeyboardButton(text="📚 Как пользоваться", callback_data="info_how"))
    builder.row(InlineKeyboardButton(text="❓ FAQ", callback_data="info_faq"))
    builder.row(InlineKeyboardButton(text="👤 Об авторе", callback_data="info_author"))
    builder.row(InlineKeyboardButton(
        text="📢 Telegram-канал Recovery Lab",
        url="https://t.me/+x6O0l82YAbg3MmJi"  # ЗАМЕНИТЬ НА РЕАЛЬНЫЙ
    ))
    builder.row(InlineKeyboardButton(
        text="💬 Чат Recovery Lab",
        url="https://t.me/+ZFkkMxkM4PsyNWFi"  # ЗАМЕНИТЬ НА РЕАЛЬНЫЙ
    ))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    
    return builder.as_markup()


def get_practices_list(practices: list, back_callback: str) -> InlineKeyboardMarkup:
    """Список практик с кнопками"""
    builder = InlineKeyboardBuilder()
    
    for practice in practices:
        builder.row(InlineKeyboardButton(
            text=f"▶️ {practice['title']}",
            callback_data=f"practice_{practice['id']}"
        ))
    
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=back_callback))
    
    return builder.as_markup()


def get_subscription_keyboard(price: int) -> InlineKeyboardMarkup:
    """Клавиатура для оформления подписки"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text=f"💳 Оплатить {price}₽", callback_data="pay"))
    builder.row(InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu"))
    
    return builder.as_markup()


def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для оплаты"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment_confirm"))
    builder.row(InlineKeyboardButton(text="❌ Отменить", callback_data="menu"))
    
    return builder.as_markup()


def get_admin_keyboard() -> InlineKeyboardMarkup:
    """Админская клавиатура"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"))
    builder.row(InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users"))
    
    return builder.as_markup()
