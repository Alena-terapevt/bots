"""Middleware для логирования всех действий"""

import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    """Middleware для логирования всех действий пользователей"""
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Логирование действия"""
        
        user = event.from_user
        user_info = f"{user.id} (@{user.username})" if user.username else str(user.id)
        
        if isinstance(event, Message):
            logger.info(f"Message from {user_info}: {event.text[:50] if event.text else 'no text'}")
        elif isinstance(event, CallbackQuery):
            logger.info(f"Callback from {user_info}: {event.data}")
        
        return await handler(event, data)
