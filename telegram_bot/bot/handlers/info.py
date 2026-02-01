"""Handler для раздела Информация"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import get_info_menu, get_back_button
from bot.utils.texts import (
    INFO_TEXT, ABOUT_PROJECT, HOW_TO_USE, FAQ_TEXT, ABOUT_AUTHOR
)

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "info")
async def show_info(callback: CallbackQuery):
    """Показать меню Информация"""
    
    await callback.message.edit_text(
        INFO_TEXT,
        reply_markup=get_info_menu()
    )
    
    await callback.answer()


@router.callback_query(F.data == "info_about")
async def show_about_project(callback: CallbackQuery):
    """О проекте"""
    
    await callback.message.edit_text(
        ABOUT_PROJECT,
        reply_markup=get_back_button("info")
    )
    
    await callback.answer()


@router.callback_query(F.data == "info_how")
async def show_how_to_use(callback: CallbackQuery):
    """Как пользоваться"""
    
    await callback.message.edit_text(
        HOW_TO_USE,
        reply_markup=get_back_button("info")
    )
    
    await callback.answer()


@router.callback_query(F.data == "info_faq")
async def show_faq(callback: CallbackQuery):
    """FAQ"""
    
    await callback.message.edit_text(
        FAQ_TEXT,
        reply_markup=get_back_button("info")
    )
    
    await callback.answer()


@router.callback_query(F.data == "info_author")
async def show_about_author(callback: CallbackQuery):
    """Об авторе"""
    
    await callback.message.edit_text(
        ABOUT_AUTHOR,
        reply_markup=get_back_button("info")
    )
    
    await callback.answer()
