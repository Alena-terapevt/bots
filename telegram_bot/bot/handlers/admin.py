"""Handler для админской панели"""

import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.keyboards.inline import get_admin_keyboard, get_back_to_menu
from bot.database.sheets import sheets_manager
from bot.filters.admin import IsAdmin

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("admin"), IsAdmin())
async def show_admin_panel(message: Message):
    """Показать админ-панель"""
    
    text = """
👨‍💼 <b>Админ-панель</b>

Добро пожаловать в панель управления ботом!
"""
    
    await message.answer(
        text,
        reply_markup=get_admin_keyboard()
    )


@router.callback_query(F.data == "admin_stats", IsAdmin())
async def show_stats(callback: CallbackQuery):
    """Показать статистику"""
    
    try:
        # Получаем данные из Google Sheets
        all_users = sheets_manager.get_all_users()
        
        total_users = len(all_users)
        paid_users = sum(1 for u in all_users if u.get('payment_status', '').upper() == 'TRUE')
        
        # Считаем статусы
        statuses = {}
        for user in all_users:
            status = user.get('status', 'неизвестен')
            statuses[status] = statuses.get(status, 0) + 1
        
        text = f"""
📊 <b>Статистика бота</b>

<b>Всего пользователей:</b> {total_users}
<b>С активной подпиской:</b> {paid_users}
<b>Конверсия:</b> {(paid_users/total_users*100 if total_users > 0 else 0):.1f}%

<b>По статусам:</b>
"""
        
        for status, count in statuses.items():
            text += f"• {status}: {count}\n"
        
        text += "\n<i>Данные из Google Sheets</i>"
        
    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        text = "❌ Ошибка при получении статистики. Проверьте подключение к Google Sheets."
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data == "admin_users", IsAdmin())
async def show_users(callback: CallbackQuery):
    """Показать список пользователей"""
    
    try:
        all_users = sheets_manager.get_all_users()
        
        if not all_users:
            text = "👥 <b>Пользователи</b>\n\nПока нет зарегистрированных пользователей."
        else:
            text = f"👥 <b>Пользователи ({len(all_users)})</b>\n\n"
            
            # Показываем последних 10 пользователей
            for user in all_users[-10:]:
                username = user.get('username', 'нет username')
                first_name = user.get('first_name', 'Без имени')
                status = user.get('status', 'неизвестен')
                payment = '✅' if user.get('payment_status', '').upper() == 'TRUE' else '❌'
                
                text += f"{payment} {first_name} (@{username}) - {status}\n"
            
            if len(all_users) > 10:
                text += f"\n<i>Показаны последние 10 из {len(all_users)}</i>"
            
            text += "\n\n<i>Полный список в Google Sheets</i>"
    
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        text = "❌ Ошибка при получении пользователей. Проверьте подключение к Google Sheets."
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data == "admin_broadcast", IsAdmin())
async def show_broadcast(callback: CallbackQuery):
    """Рассылка"""
    
    text = """
📤 <b>Рассылка сообщений</b>

<i>Функция рассылки будет добавлена в следующей версии.</i>

Сейчас вы можете отправлять сообщения пользователям вручную, 
используя их ID из Google Sheets.
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=get_back_to_menu()
    )
    
    await callback.answer()
