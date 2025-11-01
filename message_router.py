from telegram import Update
from telegram.ext import ContextTypes
from item_qpt import gpt_question_response
from item_talk import message_handler
from item_quiz import quiz_answer_handler
from messages_random import interpret_random_input, show_funny_response
from item_translator import translator_message_handler

async def message_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("conversation_state")

    if state == "gpt":
        await gpt_question_response(update, context)
    elif state == "talk":
        await message_handler(update, context)
    elif state == "quiz":
        await quiz_answer_handler(update, context)
    elif state == "translator":  # Додаємо обробку для перекладу
        await translator_message_handler(update, context)
    else:
        # Передаємо текст повідомлення як другий аргумент
        message_text = update.message.text
        handled = await interpret_random_input(update, message_text)
        if not handled:
            await show_funny_response(update, context)