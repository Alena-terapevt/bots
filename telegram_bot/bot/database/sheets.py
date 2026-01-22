"""Интеграция с Google Sheets для CRM"""

import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any

try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    GSPREAD_AVAILABLE = True
except ImportError:
    GSPREAD_AVAILABLE = False
    logging.warning("gspread not installed, Google Sheets integration disabled")

from config.config import Config

logger = logging.getLogger(__name__)


class GoogleSheetsManager:
    """Менеджер для работы с Google Sheets"""
    
    HEADERS = [
        'user_id', 'username', 'first_name', 'last_name', 'phone',
        'date_registered', 'status', 'subscription_start', 'subscription_end',
        'payment_status', 'last_activity', 'materials_viewed',
        'problems_selected', 'consultation_requests', 'notes'
    ]
    
    def __init__(self):
        self.config = Config()
        self.client = None
        self.sheet = None
        self._init_sheet()
    
    def _init_sheet(self):
        """Инициализация подключения к Google Sheets"""
        if not GSPREAD_AVAILABLE:
            logger.warning("Google Sheets integration disabled")
            return
        
        if not self.config.GOOGLE_SHEETS_CREDENTIALS or not self.config.GOOGLE_SHEET_ID:
            logger.warning("Google Sheets credentials not configured")
            return
        
        try:
            # Парсим credentials из JSON строки (для Render secrets)
            credentials_dict = json.loads(self.config.GOOGLE_SHEETS_CREDENTIALS)
            
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = ServiceAccountCredentials.from_json_keyfile_dict(
                credentials_dict, scope
            )
            
            self.client = gspread.authorize(credentials)
            self.sheet = self.client.open_by_key(self.config.GOOGLE_SHEET_ID).sheet1
            
            # Проверяем/создаем заголовки
            self._ensure_headers()
            
            logger.info("Google Sheets connected successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            self.client = None
            self.sheet = None
    
    def _ensure_headers(self):
        """Проверяем и создаем заголовки таблицы"""
        if not self.sheet:
            return
        
        try:
            first_row = self.sheet.row_values(1)
            if not first_row or first_row != self.HEADERS:
                self.sheet.insert_row(self.HEADERS, 1)
                logger.info("Headers created in Google Sheets")
        except Exception as e:
            logger.error(f"Failed to ensure headers: {e}")
    
    def add_user(self, user_data: Dict[str, Any]) -> bool:
        """Добавить нового пользователя"""
        if not self.sheet:
            return False
        
        try:
            # Проверяем, есть ли уже такой пользователь
            existing = self.get_user(user_data['user_id'])
            if existing:
                logger.info(f"User {user_data['user_id']} already exists")
                return True
            
            # Подготавливаем данные
            row = [
                str(user_data.get('user_id', '')),
                user_data.get('username', ''),
                user_data.get('first_name', ''),
                user_data.get('last_name', ''),
                user_data.get('phone', ''),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # date_registered
                'новый',  # status
                '',  # subscription_start
                '',  # subscription_end
                'FALSE',  # payment_status
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # last_activity
                '0',  # materials_viewed
                '',  # problems_selected
                '0',  # consultation_requests
                ''  # notes
            ]
            
            self.sheet.append_row(row)
            logger.info(f"User {user_data['user_id']} added to Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add user to Google Sheets: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получить данные пользователя"""
        if not self.sheet:
            return None
        
        try:
            # Ищем пользователя по user_id (первая колонка)
            cell = self.sheet.find(str(user_id))
            if not cell:
                return None
            
            row_values = self.sheet.row_values(cell.row)
            
            # Собираем данные в словарь
            user_data = {}
            for i, header in enumerate(self.HEADERS):
                user_data[header] = row_values[i] if i < len(row_values) else ''
            
            return user_data
            
        except Exception as e:
            logger.error(f"Failed to get user from Google Sheets: {e}")
            return None
    
    def update_user(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Обновить данные пользователя"""
        if not self.sheet:
            return False
        
        try:
            cell = self.sheet.find(str(user_id))
            if not cell:
                logger.warning(f"User {user_id} not found in Google Sheets")
                return False
            
            row_num = cell.row
            
            # Обновляем только нужные колонки
            for key, value in updates.items():
                if key in self.HEADERS:
                    col_num = self.HEADERS.index(key) + 1
                    self.sheet.update_cell(row_num, col_num, str(value))
            
            # Обновляем last_activity
            activity_col = self.HEADERS.index('last_activity') + 1
            self.sheet.update_cell(
                row_num, 
                activity_col, 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            logger.info(f"User {user_id} updated in Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update user in Google Sheets: {e}")
            return False
    
    def check_payment_status(self, user_id: int) -> bool:
        """Проверить статус оплаты пользователя"""
        if not self.sheet:
            return False
        
        try:
            user_data = self.get_user(user_id)
            if not user_data:
                return False
            
            # Проверяем payment_status (TRUE/FALSE)
            payment_status = user_data.get('payment_status', 'FALSE').upper()
            
            # Также проверяем дату окончания подписки
            subscription_end = user_data.get('subscription_end', '')
            if subscription_end:
                try:
                    end_date = datetime.strptime(subscription_end, '%Y-%m-%d %H:%M:%S')
                    if datetime.now() > end_date:
                        # Подписка истекла
                        self.update_user(user_id, {
                            'payment_status': 'FALSE',
                            'status': 'истек'
                        })
                        return False
                except ValueError:
                    pass
            
            return payment_status == 'TRUE'
            
        except Exception as e:
            logger.error(f"Failed to check payment status: {e}")
            return False
    
    def set_subscription(self, user_id: int, days: int = 30) -> bool:
        """Установить подписку пользователю"""
        if not self.sheet:
            return False
        
        try:
            start_date = datetime.now()
            end_date = start_date.replace(day=start_date.day + days)
            
            updates = {
                'payment_status': 'TRUE',
                'status': 'активная подписка',
                'subscription_start': start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'subscription_end': end_date.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return self.update_user(user_id, updates)
            
        except Exception as e:
            logger.error(f"Failed to set subscription: {e}")
            return False
    
    def increment_counter(self, user_id: int, field: str) -> bool:
        """Увеличить счетчик (materials_viewed, consultation_requests)"""
        if not self.sheet:
            return False
        
        try:
            user_data = self.get_user(user_id)
            if not user_data:
                return False
            
            current_value = int(user_data.get(field, '0'))
            return self.update_user(user_id, {field: current_value + 1})
            
        except Exception as e:
            logger.error(f"Failed to increment counter: {e}")
            return False
    
    def add_problem(self, user_id: int, problem: str) -> bool:
        """Добавить проблему в список"""
        if not self.sheet:
            return False
        
        try:
            user_data = self.get_user(user_id)
            if not user_data:
                return False
            
            problems = user_data.get('problems_selected', '')
            problems_list = problems.split(', ') if problems else []
            
            if problem not in problems_list:
                problems_list.append(problem)
            
            return self.update_user(user_id, {
                'problems_selected': ', '.join(problems_list)
            })
            
        except Exception as e:
            logger.error(f"Failed to add problem: {e}")
            return False
    
    def get_all_users(self) -> list:
        """Получить всех пользователей"""
        if not self.sheet:
            return []
        
        try:
            all_records = self.sheet.get_all_records()
            return all_records
        except Exception as e:
            logger.error(f"Failed to get all users: {e}")
            return []


# Singleton instance
sheets_manager = GoogleSheetsManager()
