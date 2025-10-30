from telegram import Update
from telegram.ext import ContextTypes
from util import (send_text, load_prompt, send_text_buttons, send_image)
from gpt import ChatGptService
from credentials import ChatGPT_TOKEN
import logging
from menu_handler import start
from item_buttons import RANDOM_BUTTONS, get_keyboard

chat_gpt = ChatGptService(ChatGPT_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Обробник команди /random для отримання випадкового факту
async def random_fact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Універсальний доступ до повідомлення
        message_obj = update.effective_message
        chat_id = update.effective_chat.id

        # Надсилаємо заздалегідь підготовлене зображення
        await send_image(update, context, 'item_random')

        # Відправляємо повідомлення про очікування відповіді від ChatGPT
        waiting_message = await send_text(update, context, "Шукаю цікавий факт для вас ...")

        #Завантажуємо заздалегідь підготовлений промпт для випадкового факту
        prompt = load_prompt('item_random')

        # Отримуємо факт від ChatGPT
        fact = await chat_gpt.send_question(prompt, "Розкажи мені цікавий факт")

        # Видаляємо повідомлення "Шукаю факт..."
        if waiting_message:
            await context.bot.delete_message(chat_id=chat_id, message_id=waiting_message.message_id)

        # Створюємо клавітуру
        keyboard = get_keyboard(RANDOM_BUTTONS)

        # Відправляємо результат
        await send_text_buttons(update, context, f"*Випадковий факт:*\n\n{fact}", RANDOM_BUTTONS)

    except Exception as e:
        logger.error(f"Помилка при отримані випадкового факту: {e}")
        # Надсилаєм повідомлення про помилку
        await send_text(update, context, "Нажаль виникла помилка при отримані факту. Спробуйте ще раз пізніше.")

        # Видаляємо повідомлення про очікування в разі помилки
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

# Користувацький обробник колбеків для кнопок випадкових фактів
async def random_fact_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer() #Обов'язково відповідаємо на кашбек

    #Отримуємо дані з колбеку
    if data == 'random':
        # Якщо натиснути кнопку "Хочу ще факт"
        await random_fact(update, context)
    elif data == 'start':
        # Якщо натиснути кнопку "Закінчити"
        await start(update, context)







