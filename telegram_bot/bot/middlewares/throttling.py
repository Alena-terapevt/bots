"""Middleware для защиты от спама (rate limiting)"""

import logging
from typing import Callable, Dict, Any, Awaitable
from datetime import datetime, timedelta
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from config.config import Config

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    """Middleware для ограничения частоты запросов"""
    
    def __init__(self):
        self.config = Config()
        self.user_timestamps: Dict[int, datetime] = {}
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Проверка rate limit"""
        
        user_id = event.from_user.id
        now = datetime.now()
        
        # Проверяем последний запрос пользователя
        if user_id in self.user_timestamps:
            last_request = self.user_timestamps[user_id]
            time_passed = (now - last_request).total_seconds()
            
            # Если прошло меньше 0.5 секунд с последнего запроса
            if time_passed < 0.5:
                logger.warning(f"Rate limit exceeded for user {user_id}")
                
                # Для callback query отвечаем alert
                if isinstance(event, CallbackQuery):
                    await event.answer(
                        "⏱ Подождите немного перед следующим действием",
                        show_alert=True
                    )
                return
        
        # Обновляем timestamp
        self.user_timestamps[user_id] = now
        
        # Очищаем старые timestamps (старше 1 минуты)
        cutoff_time = now - timedelta(minutes=1)
        self.user_timestamps = {
            uid: ts for uid, ts in self.user_timestamps.items()
            if ts > cutoff_time
        }
        
        return await handler(event, data)
