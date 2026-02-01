"""Handler для главного меню"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import get_main_menu
from bot.utils.texts import MAIN_MENU_TEXT

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "menu")
async def show_menu(callback: CallbackQuery):
    """Показать главное меню"""
    
    await callback.message.edit_text(
        MAIN_MENU_TEXT,
        reply_markup=get_main_menu()
    )
    
    await callback.answer()
