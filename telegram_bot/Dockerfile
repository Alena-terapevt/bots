FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание директорий для логов
RUN mkdir -p logs

# Добавляем /app в PYTHONPATH
ENV PYTHONPATH=/app

# Запуск бота из корня проекта
CMD ["python", "-m", "bot.main"]
