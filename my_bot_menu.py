from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from credentials import BOT_TOKEN
from menu_handler import start
from item_random import random_fact, random_fact_button_handler
from item_question import gpt_handler,  gpt_question_response, end_conversation_button
from item_talk import talk_handler, talk_button_handler, message_handler
from item_error_gpt import error_gpt
from messages_random import interpret_random_input, show_funny_response
from telegram.ext import ContextTypes

# створення додатку
app = ApplicationBuilder().token(BOT_TOKEN).build()

# реєстрація обробників
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random_fact))
#відловлює при натисканні кнопки (хочу ще факт чи старт)
app.add_handler(CallbackQueryHandler(random_fact_button_handler, pattern="^(random|start)$"))


# Запуск команди (задати питання ChatGPT)
app.add_handler(CommandHandler('gpt', gpt_handler))
#Запуск при натисканні кнопки "Закінчити"
app.add_handler(CallbackQueryHandler(end_conversation_button, pattern="^start$"))

#Запуск команд для діалогу з відомою особистістю (item_talk)
app.add_handler(CommandHandler('talk', talk_handler))
app.add_handler(CallbackQueryHandler(talk_button_handler, pattern="^talk_|^start$"))
#  Обробник повідомлень під час розмови з особистістю
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Всі повідомлення тексту — передаються у ChatGPT (якщо користувач у стані 'gpt')
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_question_response))


async def fallback_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Викликається, якщо повідомлення не відповідає жодному стану."""
    handled = await interpret_random_input(update, context)
    if not handled:
        await show_funny_response(update, context)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, interpret_random_input))

# Реєструємо обробник помилок
app.add_error_handler(error_gpt)

# запуск
app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
