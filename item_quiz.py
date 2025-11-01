from telegram import Update
from telegram.ext import ContextTypes
from util import (send_text, load_prompt, send_image)
from gpt import ChatGptService
from credentials import ChatGPT_TOKEN
import logging
from menu_handler import start
from item_error_gpt import error_gpt
from item_buttons import QUIZ_BUTTONS, QUIZ_ACTION_BUTTONS, get_keyboard,QUIZ_EXIT_BUTTONS

chat_gpt = ChatGptService(ChatGPT_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Обробник команди /quiz
async def quiz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Надсилаємо заздалегідь підготовлене зображення
    await send_image(update, context, 'quiz')

    # Відображення кнопок з темами
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Виберіть тему нижче:",
        reply_markup=get_keyboard({**QUIZ_BUTTONS, **QUIZ_EXIT_BUTTONS})
    )
# Обераємо тему
async def quiz_topic_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Обробляємо обрану тему
    query = update.callback_query
    await query.answer()

    #Дія при натисканні кнопки
    topic_key = query.data
    # ✅ реагуємо тільки на кнопки тем
    if not topic_key.startswith("topic_"):
        return  # не чіпаємо інші кнопки

    # беремо name
    topic_name = QUIZ_BUTTONS[topic_key]

    context.user_data["conversation_state"] = "quiz"
    context.user_data["quiz_topic"] = topic_name
    context.user_data["quiz_score"] = 0

    await send_text(update, context, f"Тема вибрана: {topic_name}\nГенерую питання ...")
    await ask_question(update, context)

#Генерація питання
async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = context.user_data.get("quiz_topic")
    if not topic:
        await send_text(update, context, "Спершу оберіть тему квізу командою /quiz.")
        return

    base_prompt = load_prompt("quiz")
    prompt = f"{base_prompt}\nТема: {topic}"

    # встановлюємо system prompt
    chat_gpt.set_prompt(prompt)

    # отримуємо питання
    question_text = await chat_gpt.add_message(topic)

    logger.info(f"GPT запит: {topic}")
    logger.info(f"GPT відповідь: {question_text}")

    if not question_text:
        await send_text(update, context, "Помилка GPT: не отримано питання. Спробуйте ще раз.")
        return

    if "Правильна відповідь" not in question_text:
        logger.error("GPT згенерував питання без правильного варіанту. Перегенерую...")
        return await ask_question(update, context)

    context.user_data["quiz_question"] = question_text
    # Надсилаємо питання користувачу
    await send_text(update, context, question_text)
    await send_text(update, context, "Напишіть вашу відповідь нижче (букву або слово):")


#  Обробка відповіді користувача
async def quiz_answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["conversation_state"] = "quiz"

    message = update.effective_message
    if not message:
        return

    answer = message.text.lower()

    user_answer = update.message.text.strip()
    question = context.user_data.get("quiz_question")

    if not question:
        await send_text(update, context, "Спочатку запустіть квіз командою /quiz.")
        return

    # Створюємо prompt для перевірки відповіді GPT
    check_prompt = (
        f"Перевір правильність відповіді користувача.\n"
        f"Питання:\n{question}\n"
        f"Відповідь користувача: {user_answer}\n"
        "Відповідь дай СТРОГО одним рядком:\n"
        "✅ Правильно!\n"
        "або\n"
        "❌ Неправильно. Вкажи правильну відповідь."
    )

    # Встановлюємо системний prompt
    #chat_gpt.set_prompt(check_prompt)

    try:
        # Відправляємо повідомлення користувача і отримуємо результат від GPT
        full_prompt = f"{check_prompt}\n\nВідповідь користувача: {user_answer}"
        result_text = await chat_gpt.add_message(full_prompt)
    except Exception as e:
        context.error = e
        await error_gpt(update, context)
        return

    # Перевірка на порожню або некоректну відповідь
    if not result_text or result_text.strip() == "":
        await send_text(update, context, "GPT не повернув результат. Спробуйте ще раз.")
        return

    # Підрахунок балів
    if "✅" in result_text:
        context.user_data["quiz_score"] = context.user_data.get("quiz_score", 0) + 1

    score = context.user_data.get("quiz_score", 0)
    await send_text(update, context, f"{result_text}\n\n🏆 Ваш рахунок: {score}")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Що робимо далі?",
        reply_markup=get_keyboard(QUIZ_ACTION_BUTTONS)
    )


# Обробка кнопок дій після відповіді
async def quiz_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

   # Обробляє кнопки після відповіді
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "quiz_next":
        await ask_question(update, context)

    elif data == "quiz_change":
        await quiz_handler(update, context)
        return

    elif data == "quiz_end":
        score = context.user_data.get("quiz_score", 0)
        await send_text(update, context, f"✅ Квіз завершено!\nВаш фінальний рахунок: {score}")

        # Очищаємо стан квізу
        context.user_data.pop("quiz_topic", None)
        context.user_data.pop("quiz_question", None)
        context.user_data.pop("quiz_score", None)
        context.user_data["conversation_state"] = None

        # Викликаємо головне меню
        await start(update, context)













