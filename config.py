import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# API ключи из переменных окружения
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
CHATGPT_API_KEY = os.getenv('OPENAI_API_KEY')

if not DEEPSEEK_API_KEY or not CHATGPT_API_KEY:
    print("Ошибка: API ключи не найдены. Пожалуйста, создайте файл .env с ключами:")
    print("DEEPSEEK_API_KEY=ваш_ключ_deepseek")
    print("OPENAI_API_KEY=ваш_ключ_openai")
    exit(1)

# Настройки моделей
MODELS = {
    'deepseek': {
        'model': 'deepseek-chat',
        'base_url': 'https://api.deepseek.com/v1'
    },
    'chatgpt': {
        'model': 'gpt-3.5-turbo',
        'base_url': 'https://api.openai.com/v1'
    }
}