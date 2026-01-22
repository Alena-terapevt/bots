import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import start, menu, materials, problems, payment, contacts, booking, reviews, admin
from bot.middlewares.subscription import SubscriptionMiddleware
from bot.middlewares.logging import LoggingMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from config.config import Config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    
    # Загрузка конфигурации
    config = Config()
    
    # Инициализация бота
    bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
    
    # Storage для FSM (используем Memory, если Redis недоступен)
    try:
        storage = RedisStorage.from_url(
            f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}"
        )
        logger.info("Using Redis storage")
    except Exception as e:
        logger.warning(f"Redis unavailable, using Memory storage: {e}")
        storage = MemoryStorage()
    
    dp = Dispatcher(storage=storage)
    
    # Регистрация middlewares
    dp.message.middleware(LoggingMiddleware())
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(SubscriptionMiddleware())
    
    dp.callback_query.middleware(LoggingMiddleware())
    dp.callback_query.middleware(SubscriptionMiddleware())
    
    # Регистрация handlers
    dp.include_router(start.router)
    dp.include_router(menu.router)
    dp.include_router(materials.router)
    dp.include_router(problems.router)
    dp.include_router(payment.router)
    dp.include_router(contacts.router)
    dp.include_router(booking.router)
    dp.include_router(reviews.router)
    dp.include_router(admin.router)
    
    logger.info("Bot started successfully")
    
    # Запуск polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
