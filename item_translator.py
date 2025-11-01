from telegram import Update
from telegram.ext import ContextTypes
from util import send_text, send_text_buttons
from gpt import ChatGptService
from credentials import ChatGPT_TOKEN
import logging
from item_buttons import LANG_BUTTONS, TRANSLATE_CONTINUE_BUTTONS
from menu_handler import start

chat_gpt = ChatGptService(ChatGPT_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Обробник перекладу — отримуємо текст від користувача
async def translator_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отримуємо текст повідомлення та дані користувача
    user_data = context.user_data
    message_text = update.message.text

    # Якщо мова ще не вибрана — показуємо кнопки вибору мови
    if 'translator_language' not in user_data:
        # Очікуємо, що callback обробить вибір мови
        await send_text_buttons(update, context, "Виберіть мову для перекладу:", LANG_BUTTONS)
        return

    # Якщо мова вибрана — перекладаємо текст
    target_lang = user_data['translator_language']

    # Підготовка prompt для ChatGPT
    prompt = f"Переклади наступний текст на {target_lang}:\n\n{message_text}"

    #Надсилаємо повідомлення "Перекладаю..."
    waiting_message = await send_text(update, context, "Перекладаю текст...")

    try:
        # Отримуємо переклад від GPT
        translated_text = await chat_gpt.add_message(prompt)
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

        # Надсилаємо переклад із кнопками
        await send_text_buttons(
            update,
            context,
            f"🌍 Переклад ({target_lang}):\n\n{translated_text}",
            TRANSLATE_CONTINUE_BUTTONS
        )

    except Exception as e:
        logger.error(f"Помилка перекладу: {e}")
        await send_text(update, context, "На жаль, сталася помилка при перекладі. Спробуйте ще раз.")
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)


# Обробник кнопок для перекладача
async def translator_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_data = context.user_data

    # Кнопка "Закінчити" — повертаємося в меню
    if data == 'start':
        user_data.pop('conversation_state', None)
        user_data.pop('translator_language', None)
        await start(update, context)
        return

    # Кнопка "Змінити мову" — очищаємо вибір мови
    if data == 'translator_change':
        user_data.pop('translator_language', None)
        await send_text_buttons(update, context, "Виберіть нову мову для перекладу:", LANG_BUTTONS)
        return

    # Якщо обрана мова
    if data.startswith('lang_'):
        # Зберігаємо вибрану мову
        lang_name = LANG_BUTTONS[data]
        user_data['translator_language'] = lang_name
        user_data['conversation_state'] = 'translator'
        await send_text(update, context, f"Ви обрали мову: *{lang_name}*\nНадішліть текст для перекладу.")
