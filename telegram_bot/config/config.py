import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Конфигурация приложения"""
    
    # Telegram Bot
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '')
    ADMIN_ID: int = int(os.getenv('ADMIN_ID', '0'))
    
    # Database
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///bot.db')
    
    # Redis
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB: int = int(os.getenv('REDIS_DB', '0'))
    
    # Google Sheets
    GOOGLE_SHEETS_CREDENTIALS: str = os.getenv('GOOGLE_SHEETS_CREDENTIALS', '')
    GOOGLE_SHEET_ID: str = os.getenv('GOOGLE_SHEET_ID', '')
    
    # Payment
    PAYMENT_PROVIDER_TOKEN: str = os.getenv('PAYMENT_PROVIDER_TOKEN', '')
    TEST_PAYMENT: bool = os.getenv('TEST_PAYMENT', 'True').lower() == 'true'
    
    # App Settings
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Subscription
    SUBSCRIPTION_PRICE: int = int(os.getenv('SUBSCRIPTION_PRICE', '20'))  # В рублях
    SUBSCRIPTION_DURATION_DAYS: int = int(os.getenv('SUBSCRIPTION_DURATION_DAYS', '30'))
    
    # Limits
    RATE_LIMIT_REQUESTS: int = int(os.getenv('RATE_LIMIT_REQUESTS', '5'))
    RATE_LIMIT_PERIOD: int = int(os.getenv('RATE_LIMIT_PERIOD', '60'))
    
    # Welcome video file_id (оставляем пустым, заполнишь потом)
    WELCOME_VIDEO_FILE_ID: str = os.getenv('WELCOME_VIDEO_FILE_ID', '')
