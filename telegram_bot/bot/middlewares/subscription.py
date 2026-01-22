"""Middleware для проверки подписки"""

import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.database.sheets import sheets_manager

logger = logging.getLogger(__name__)


class SubscriptionMiddleware(BaseMiddleware):
    """Middleware для проверки активной подписки"""
    
    # Действия, которые не требуют подписки
    FREE_ACTIONS = [
        'menu', 'start', 'help', 'problems', 'contacts', 'booking',
        'reviews', 'subscribe', 'subscribe_info', 'pay', 'payment_confirm'
    ]
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        """Проверка подписки перед выполнением handler"""
        
        # Определяем user_id
        user_id = event.from_user.id
        
        # Для callback query проверяем action
        if isinstance(event, CallbackQuery):
            callback_data = event.data
            
            # Проверяем, требует ли действие подписку
            requires_subscription = self._requires_subscription(callback_data)
            
            if requires_subscription:
                # Проверяем статус подписки в Google Sheets
                has_access = sheets_manager.check_payment_status(user_id)
                
                if not has_access:
                    logger.info(f"User {user_id} tried to access paid content without subscription")
                    # Сохраняем информацию о том, что нужна подписка
                    data['requires_subscription'] = True
                else:
                    data['requires_subscription'] = False
                    logger.info(f"User {user_id} has active subscription")
            else:
                data['requires_subscription'] = False
        else:
            data['requires_subscription'] = False
        
        # Продолжаем выполнение handler
        return await handler(event, data)
    
    def _requires_subscription(self, callback_data: str) -> bool:
        """Проверяет, требует ли callback подписку"""
        
        # Проверяем, начинается ли callback с бесплатных действий
        for free_action in self.FREE_ACTIONS:
            if callback_data.startswith(free_action):
                return False
        
        # Если это доступ к материалам, требуется подписка
        if any(keyword in callback_data for keyword in [
            'material', 'format_', 'materials_theme', 'materials_popular',
            'get_material'
        ]):
            return True
        
        return False
