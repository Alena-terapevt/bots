"""Handler для главного меню"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import get_main_menu
from bot.utils.texts import MAIN_MENU_TEXT, HELP_TEXT

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "help")
async def show_help(callback: CallbackQuery):
    """Показать справку"""
    
    await callback.message.edit_text(
        HELP_TEXT,
        reply_markup=get_main_menu()
    )
    
    await callback.answer()
