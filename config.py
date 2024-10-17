# config.py
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена из переменных окружения
TOKEN = os.getenv('TELEGRAM_TOKEN')