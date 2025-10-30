from telegram import Update
from telegram.ext import ContextTypes
from util import (send_text, load_prompt, send_image, send_text_buttons)
from gpt import ChatGptService
from credentials import ChatGPT_TOKEN
import logging
from item_buttons import get_keyboard, PERSON_BUTTONS
from menu_handler import start
from messages_random import interpret_random_input, show_funny_response
chat_gpt = ChatGptService(ChatGPT_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Обробник команди /talk для діалогу з відомими особистостями
async def talk_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Очищення попередніх станів розмови
        context.user_data.clear()

        # Надсилаємо заздалегідь підготовлене зображення
        await send_image(update, context, 'talk')

        # Створюємо клавітуру
        keyboard = get_keyboard(PERSON_BUTTONS)

        # Надсилаємо повідомлення з вибором особистості
        await send_text_buttons(update, context, "👤 Виберіть особистість, з якою ви хочете поспілкуватися:", PERSON_BUTTONS)
    except Exception as e:
       logger.error(f"Помилка при запуску GPT-діалогу: {e}")
       # Надсилаємо повідомлення про помилку
       await send_text(update, context, "Нажаль виникла помилка при вибору особистості. Спробуйте ще раз пізніше.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Отримуємо текст повідомлення від користувача
    message_text = update.message.text

    # Перевіряємо поточний стан розмови
    conversation_state = context.user_data.get('conversation_state')

    # Якщо стан розмови не визначено (випадкове повідомлення)
    if not conversation_state:
        # Спробуємо інтерпретувати намір користувача
        intent_recognized = await interpret_random_input(update, context, message_text)

        # Якщо намір не визначено, показуємо кумедну відповідь
        if not intent_recognized:
            await show_funny_response(update, context)

        return

    # Обробка питання до ChatGPT
    if conversation_state == 'gpt':
        # Відправляємо повідомлення про очікування відповіді
        waiting_message = await send_text(update, context, "🔍 Обробляю ваше питання...")

        try:
            # Надсилаємо запит до ChatGPT
            response = await chat_gpt.add_message(message_text)

            # Видаляємо повідомлення про очікування
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

            # Надсилаємо відповідь користувачу
            await send_text(update, context, f"Відповідь ChatGPT:*\n\n{response}")

        except Exception as e:
            logger.error(f"Помилка при отриманні відповіді від ChatGPT: {e}")
            await send_text(update, context, "На жаль, виникла помилка при отриманні відповіді. Спробуйте ще раз пізніше.")
            # Видаляємо повідомлення про очікування в разі помилки
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

    elif conversation_state == 'talk':
        # Обробка повідомлення для діалогу з обраною особистістю
        # Отримуємо обрану особистість
        personality = context.user_data.get('selected_personality')

        if not personality:
            await send_text(update, context, "Будь ласка, спочатку виберіть особистість для розмови за допомогою команди /talk")
            return

        # Відправляємо повідомлення про очікування відповіді
        waiting_message = await send_text(update, context, "Обробляю ваше повідомлення...")

        try:
            # Надсилаємо запит до ChatGPT з промптом обраної особистості
            response = await chat_gpt.add_message(message_text)

            # Видаляємо повідомлення про очікування
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

            # Створюємо кнопку "Закінчити"
            buttons = {'start': 'Закінчити'}

            # Надсилаємо відповідь користувачу з кнопкою
            personality_name = personality.replace('talk_', '').capitalize()
            await send_text_buttons(update, context, f"👤 *{personality_name}:*\n\n{response}", buttons)

        except Exception as e:
            logger.error(f"Помилка при отриманні відповіді від ChatGPT: {e}")
            await send_text(update, context, "На жаль, виникла помилка при отриманні відповіді. Спробуйте ще раз пізніше.")
            # Видаляємо повідомлення про очікування в разі помилки
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waiting_message.message_id)

# Обробник колбеків для діалогу з відомими особистостями
async def talk_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # відповідоємо на callback

    # Отримуємо дані з колбеку
    data = query.data

    # Якщо натиснути кнопку "Закінчити"
    if data == 'start':
        context.user_data.pop('conversation_state', None)
        context.user_data.pop('selected_personality', None)
        await start(update, context)
        return

    # Перевіряємо, чи це вибір особистості
    if data.startswith('talk_'):
        # очищуємо попередні дані користувача перед вибором нової особистості
        context.user_data.clear()

        # Зберігаємо обрану особистість
        context.user_data['selected_personality'] = data
        context.user_data['conversation_state'] = 'talk'
        try:
            # Завершуємо промт для обраної особистості
            prompt = load_prompt(data)
            chat_gpt.set_prompt(prompt) # Це повністю скидає історію повідоммень у сервісі hatGPT
        except FileNotFoundError:
            await send_text(update, context, " Не знайдено файл для цієї особистості.")
            logger.error(f"Промт не знайдено для {data}")
            return

        # Надсилаємо повідомлення про початок розмови з вибраною особистістю
        personality_name = data.replace('talk_', '').capitalize()

        # Надсилаємо зображення обраної особистості
        await send_image(update, context, data)

        # Надсилаємо повідомлення з інструкцією та кнопкою "Закінчити"
        buttons = {'start': 'Закінчити 🏁'}
        await send_text_buttons(update, context,
                                f"👤 Ви почали розмову з *{personality_name}*. Надішліть повідомлення, щоб отримати відповідь.",
                                buttons)

        logger.info(f"Користувач {update.effective_user.first_name} розпочав розмову з {personality_name}")








