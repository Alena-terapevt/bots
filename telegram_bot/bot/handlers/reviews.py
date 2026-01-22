"""Handler для отзывов"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.keyboards.inline import get_reviews_keyboard
from bot.utils.texts import REVIEWS_TEXT

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "reviews")
async def show_reviews(callback: CallbackQuery):
    """Показать отзывы"""
    
    await callback.message.edit_text(
        REVIEWS_TEXT,
        reply_markup=get_reviews_keyboard()
    )
    
    await callback.answer()


@router.callback_query(F.data == "leave_review")
async def leave_review(callback: CallbackQuery):
    """Оставить отзыв"""
    
    text = """
✍️ <b>Оставить отзыв</b>

Напишите ваш отзыв о практиках и материалах Алёны.

Ваш отзыв поможет другим людям принять решение! 🙏

<i>Функция будет добавлена в следующей версии</i>
"""
    
    await callback.message.edit_text(
        text,
        reply_markup=get_reviews_keyboard()
    )
    
    await callback.answer()
