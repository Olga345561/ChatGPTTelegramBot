from telegram import Update
from telegram.ext import ContextTypes
from util import (send_text, load_prompt, send_image, send_text_buttons)
from gpt import ChatGptService
from credentials import ChatGPT_TOKEN
import logging
from item_buttons import get_keyboard, QUESTION_BUTTONS
from telegram.error import Conflict, NetworkError
from menu_handler import start


chat_gpt = ChatGptService(ChatGPT_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Обробник команди /question для отримання відповіді
async def gpt_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Надсилаємо заздалегідь підготовлене зображення
        await send_image(update, context, 'question')

        # Завантажуємо заздалегідь підготовлений промпт для відповіді
        prompt = load_prompt('question_txt')
        chat_gpt.set_prompt(prompt)  # Це повністю скидає історію повідомлень у сервісі GPT

        # Створюємо клавіатуру з кнопками з item_buttons.py
        keyboard = get_keyboard(QUESTION_BUTTONS)

        # Надсилаємо повідомлення з кнопкою
        await send_text_buttons(
            update,
            context,
            "Задайте питання, і я відповім вам на нього за допомогою ChatGPT. "
            "\nПросто напишіть текстове повідомлення.",
            QUESTION_BUTTONS
        )

        #Зберігаємо стан розмови у контексті користувача
        context.user_data['conversation_state'] = 'gpt'

    except Exception as e:
        logger.error(f"Помилка при запуску GPT-діалогу: {e}")
        # Надсилаємо повідомлення про помилку
        await send_text(update, context, "Нажаль виникла помилка при отримані відповіді. Спробуйте ще раз пізніше.")

#Обробник повідомлень користувача (відповідь GPT на запитання користувача)
async def gpt_question_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Перевіряємо, що користувач у мережі GPT
    if context.user_data.get('conversation_state') == 'gpt':
        user_text = update.message.text.strip()

        try:
            # Завантажуємо системний prompt
            prompt = load_prompt('question_txt')
            # Передаємо контекст у ChatGPT
            chat_gpt.set_prompt(prompt)
            # Отримуємо відповідь
            response = await chat_gpt.send_question(prompt, user_text)

            # Клавіатура з кнопкою "Закінчити"
            keyboard = get_keyboard(QUESTION_BUTTONS)

            await send_text_buttons(update, context, f"Відповідь:\n\n{response}", QUESTION_BUTTONS)


        except Exception as e:
            logger.error(f"Помилка при запиті до ChatGPT{e}")
            await send_text(update, context, "Не вдалося отримати відповідь. Спробуйте пізніше.")

# === Обробник натискання кнопки “Закінчити” ===
async def end_conversation_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data['conversation_state'] = None
    await start(update, context)

# Обробник помилок для бота
async def error_gpt(update, context):
    logger.error(f"Помилка під час обробки оновлення: {context.error}")
    if isinstance(context.error, Conflict):
        logger.error("Конфлікт: інший екземпляр цього бота вже запущено. Переконайтесь, що працює лише один екземпляр.")
    elif isinstance(context.error, NetworkError):
        logger.error(f"Помилка мережі: {context.error}")



















