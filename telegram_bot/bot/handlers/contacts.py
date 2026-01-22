"""Handler для связи с автором"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import get_back_to_menu
from bot.utils.texts import CONTACTS_TEXT

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "contacts")
async def show_contacts(callback: CallbackQuery):
    """Показать контакты эксперта"""
    
    await callback.message.edit_text(
        CONTACTS_TEXT,
        reply_markup=get_back_to_menu(),
        disable_web_page_preview=True
    )
    
    await callback.answer()
