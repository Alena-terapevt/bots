"""Фильтры для бота"""

from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from config.config import Config


class IsAdmin(Filter):
    """Фильтр для проверки, является ли пользователь админом"""
    
    def __init__(self):
        self.config = Config()
    
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        """Проверка на админа"""
        return event.from_user.id == self.config.ADMIN_ID
