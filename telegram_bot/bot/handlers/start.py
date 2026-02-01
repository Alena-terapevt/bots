"""Handler для команды /start и приветствия"""

import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline import get_main_menu
from bot.utils.texts import WELCOME_MESSAGE, WELCOME_NO_VIDEO, MAIN_MENU_TEXT
from bot.database.sheets import sheets_manager
from config.config import Config

logger = logging.getLogger(__name__)

router = Router()
config = Config()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Обработка команды /start"""
    
    user = message.from_user
    
    # Добавляем пользователя в Google Sheets
    user_data = {
        'user_id': user.id,
        'username': user.username or '',
        'first_name': user.first_name or '',
        'last_name': user.last_name or ''
    }
    
    sheets_manager.add_user(user_data)
    
    # Отправляем приветствие
    welcome_text = WELCOME_MESSAGE.format(first_name=user.first_name or "друг")
    
    # Если есть видео-приветствие, отправляем его
    if config.WELCOME_VIDEO_FILE_ID:
        try:
            await message.answer_video_note(
                video_note=config.WELCOME_VIDEO_FILE_ID
            )
        except Exception as e:
            logger.error(f"Failed to send welcome video: {e}")
    else:
        welcome_text += WELCOME_NO_VIDEO
    
    # Отправляем текст приветствия
    await message.answer(welcome_text)
    
    # Показываем главное меню
    await message.answer(
        MAIN_MENU_TEXT,
        reply_markup=get_main_menu()
    )
    
    logger.info(f"New user started bot: {user.id} (@{user.username})")
