from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from credentials import BOT_TOKEN
from menu_handler import start
from item_random import random_fact, random_fact_button_handler, error_handler
from item_question import gpt_handler,  gpt_question_response, error_gpt

# створення додатку
app = ApplicationBuilder().token(BOT_TOKEN).build()

# реєстрація обробників
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random_fact))
#відловлює натискання кнопки (хочу ще факт чи старт)
app.add_handler(CallbackQueryHandler(random_fact_button_handler, pattern="^(random|start)$"))
app.add_error_handler(error_handler)

# Запуск команди (задати питання ChatGPT)
app.add_handler(CommandHandler('gpt', gpt_handler))
# Всі повідомлення тексту — передаються у ChatGPT (якщо користувач у стані 'gpt')
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_question_response))
app.add_error_handler(error_gpt)

# запуск
app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
