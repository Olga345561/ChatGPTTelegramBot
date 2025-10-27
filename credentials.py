from dotenv import load_dotenv
import os

#Копіюємо дані з .env файлу
load_dotenv()

# Створюємо змінні для користування нашими TOKEN
ChatGPT_TOKEN = os.getenv('CHATGPT_TOKEN', '')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')