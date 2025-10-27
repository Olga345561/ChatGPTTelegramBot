from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from credentials import BOT_TOKEN
from menu_handler import start
from item_random import random_fact, random_fact_button_handler

# створення додатку
app = ApplicationBuilder().token(BOT_TOKEN).build()

# реєстрація обробників
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random_fact))
app.add_handler(CallbackQueryHandler(random_fact_button_handler, pattern="^(random|start)$"))

# запуск
app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
#