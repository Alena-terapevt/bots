"""Handler для оплаты и подписки"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from datetime import datetime

from bot.keyboards.inline import (
    get_subscription_keyboard, get_payment_keyboard, get_main_menu
)
from bot.utils.texts import (
    SUBSCRIPTION_OFFER, PAYMENT_SUCCESS, PAYMENT_REMINDER
)
from bot.database.sheets import sheets_manager
from config.config import Config

logger = logging.getLogger(__name__)

router = Router()
config = Config()


@router.callback_query(F.data == "subscribe")
async def show_subscription_offer(callback: CallbackQuery):
    """Показать предложение подписки"""
    
    user = callback.from_user
    
    text = SUBSCRIPTION_OFFER.format(price=config.SUBSCRIPTION_PRICE)
    
    await callback.message.edit_text(
        text,
        reply_markup=get_subscription_keyboard(config.SUBSCRIPTION_PRICE)
    )
    
    await callback.answer()


@router.callback_query(F.data == "subscribe_info")
async def show_subscription_info(callback: CallbackQuery):
    """Подробная информация о подписке"""
    
    text = f"""
📦 <b>Подробнее о подписке</b>

<b>Что входит:</b>
✅ Неограниченный доступ ко всем материалам
✅ 50+ видео-практик
✅ 30+ статей и методик
✅ 20+ аудио-медитаций
✅ Новые материалы каждую неделю
✅ Поддержка эксперта

<b>Стоимость:</b> {config.SUBSCRIPTION_PRICE}₽ в месяц
<b>Срок действия:</b> {config.SUBSCRIPTION_DURATION_DAYS} дней

<b>Как оплатить:</b>
1. Нажмите "Оплатить"
2. Переведите {config.SUBSCRIPTION_PRICE}₽ любым удобным способом
3. Нажмите "Я оплатил"
4. Доступ откроется автоматически после проверки

<i>💡 Сейчас идет тестовый период, поэтому оплата происходит вручную.
Скоро добавим автоматическую оплату!</i>
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=get_subscription_keyboard(config.SUBSCRIPTION_PRICE)
    )
    
    await callback.answer()


@router.callback_query(F.data == "pay")
async def process_payment(callback: CallbackQuery):
    """Обработка запроса на оплату"""
    
    user = callback.from_user
    
    # В будущем здесь будет интеграция с платежной системой
    # Пока показываем инструкцию для ручной оплаты
    
    text = f"""
💳 <b>Оплата подписки</b>

<b>Сумма:</b> {config.SUBSCRIPTION_PRICE}₽
<b>Срок:</b> {config.SUBSCRIPTION_DURATION_DAYS} дней

<b>Реквизиты для оплаты:</b>
📱 Номер карты: <code>XXXX XXXX XXXX XXXX</code>
(Нажмите чтобы скопировать)

Или переведите через:
• СБП
• ЮMoney
• Qiwi

<b>После оплаты нажмите "Я оплатил"</b>

<i>Администратор проверит оплату и активирует подписку в течение нескольких минут</i>
"""
    
    # Обновляем статус в Google Sheets
    sheets_manager.update_user(user.id, {'status': 'ожидает оплату'})
    
    await callback.message.edit_text(
        text,
        reply_markup=get_payment_keyboard()
    )
    
    # Отправляем уведомление админу
    admin_text = f"""
💰 <b>Запрос на оплату</b>

<b>От:</b> {user.first_name} {user.last_name or ''} (@{user.username or 'нет username'})
<b>ID:</b> <code>{user.id}</code>

<b>Сумма:</b> {config.SUBSCRIPTION_PRICE}₽
<b>Дата:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<i>Ожидает подтверждения оплаты</i>
"""
    
    try:
        await callback.bot.send_message(config.ADMIN_ID, admin_text)
        logger.info(f"Payment request sent to admin from user {user.id}")
    except Exception as e:
        logger.error(f"Failed to send payment request to admin: {e}")
    
    await callback.answer()


@router.callback_query(F.data == "payment_confirm")
async def confirm_payment(callback: CallbackQuery):
    """Подтверждение оплаты пользователем"""
    
    user = callback.from_user
    
    # Обновляем статус
    sheets_manager.update_user(user.id, {'status': 'подтвердил оплату'})
    
    text = """
✅ <b>Заявка принята!</b>

Администратор проверит оплату и активирует подписку в течение нескольких минут.

Вы получите уведомление, когда доступ будет открыт.

<i>Обычно проверка занимает не более 5-10 минут</i>

Спасибо за терпение! 🙏
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=get_main_menu()
    )
    
    # Уведомляем админа
    admin_text = f"""
✅ <b>Пользователь подтвердил оплату</b>

<b>От:</b> {user.first_name} {user.last_name or ''} (@{user.username or 'нет username'})
<b>ID:</b> <code>{user.id}</code>

<b>Сумма:</b> {config.SUBSCRIPTION_PRICE}₽

<b>Действия:</b>
1. Проверьте поступление оплаты
2. Откройте Google Sheets
3. Найдите пользователя {user.id}
4. Измените payment_status на TRUE

<i>После этого пользователь автоматически получит доступ!</i>
"""
    
    try:
        await callback.bot.send_message(config.ADMIN_ID, admin_text)
        logger.info(f"Payment confirmation sent to admin from user {user.id}")
    except Exception as e:
        logger.error(f"Failed to send payment confirmation to admin: {e}")
    
    await callback.answer("✅ Заявка отправлена")


# Функция для отправки напоминания об оплате (вызывается через 10 минут)
async def send_payment_reminder(bot, user_id: int, first_name: str):
    """Отправить напоминание об оплате"""
    
    # Проверяем, не оплатил ли уже
    has_paid = sheets_manager.check_payment_status(user_id)
    
    if has_paid:
        return
    
    text = PAYMENT_REMINDER.format(
        first_name=first_name,
        price=config.SUBSCRIPTION_PRICE
    )
    
    try:
        await bot.send_message(
            user_id,
            text,
            reply_markup=get_subscription_keyboard(config.SUBSCRIPTION_PRICE)
        )
        logger.info(f"Payment reminder sent to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send payment reminder to user {user_id}: {e}")
