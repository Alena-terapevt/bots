"""Handler для записи на встречу"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from datetime import datetime

from bot.keyboards.inline import get_booking_keyboard, get_back_to_menu
from bot.utils.texts import BOOKING_TEXT, BOOKING_SUCCESS
from config.config import Config

logger = logging.getLogger(__name__)

router = Router()
config = Config()


class BookingStates(StatesGroup):
    """Состояния для записи на встречу"""
    waiting_for_contacts = State()


@router.callback_query(F.data == "booking")
async def show_booking(callback: CallbackQuery):
    """Показать форму записи"""
    
    await callback.message.edit_text(
        BOOKING_TEXT,
        reply_markup=get_booking_keyboard()
    )
    
    await callback.answer()


@router.callback_query(F.data == "booking_form")
async def start_booking_form(callback: CallbackQuery, state: FSMContext):
    """Начать процесс записи"""
    
    await callback.message.edit_text(
        "📝 <b>Оставьте ваши контакты</b>\n\n"
        "Напишите ваше имя и номер телефона в формате:\n"
        "<i>Иван, +79991234567</i>",
        reply_markup=get_back_to_menu()
    )
    
    await state.set_state(BookingStates.waiting_for_contacts)
    await callback.answer()


@router.message(BookingStates.waiting_for_contacts)
async def process_booking(message: Message, state: FSMContext):
    """Обработка заявки на встречу"""
    
    user = message.from_user
    contact_info = message.text
    
    # Отправляем уведомление админу
    admin_text = f"""
🔔 <b>Новая заявка на встречу</b>

<b>От:</b> {user.first_name} {user.last_name or ''} (@{user.username or 'нет username'})
<b>ID:</b> <code>{user.id}</code>

<b>Контакты:</b>
{contact_info}

<b>Дата заявки:</b> {message.date.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    try:
        await message.bot.send_message(config.ADMIN_ID, admin_text)
        logger.info(f"Booking request sent to admin from user {user.id}")
    except Exception as e:
        logger.error(f"Failed to send booking request to admin: {e}")
    
    # Отправляем подтверждение пользователю
    await message.answer(
        BOOKING_SUCCESS,
        reply_markup=get_back_to_menu()
    )
    
    # Сбрасываем состояние
    await state.clear()
