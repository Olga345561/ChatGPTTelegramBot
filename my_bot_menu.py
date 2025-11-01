from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from credentials import BOT_TOKEN
from menu_handler import start
from item_random import random_fact, random_fact_button_handler
from item_qpt import gpt_handler, end_conversation_button
from item_talk import talk_handler, talk_button_handler
from item_error_gpt import error_gpt
from item_quiz import quiz_handler, quiz_topic_handler, quiz_callback_handler
from message_router import message_router

# створення додатку
app = ApplicationBuilder().token(BOT_TOKEN).build()

# реєстрація обробників команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("random", random_fact))
app.add_handler(CallbackQueryHandler(random_fact_button_handler, pattern="^(random|start)$"))

app.add_handler(CommandHandler('gpt', gpt_handler))
app.add_handler(CallbackQueryHandler(end_conversation_button, pattern="^start$"))

app.add_handler(CommandHandler('talk', talk_handler))
app.add_handler(CallbackQueryHandler(talk_button_handler, pattern="^talk_|^start$"))

app.add_handler(CommandHandler('quiz', quiz_handler))
app.add_handler(CallbackQueryHandler(quiz_topic_handler, pattern="^topic_"))
app.add_handler(CallbackQueryHandler(quiz_callback_handler, pattern="^(quiz_next|quiz_change|quiz_end)$"))

# Єдиний маршрутизатор для всіх текстових повідомлень
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_router))

# Реєструємо обробник помилок
app.add_error_handler(error_gpt)

# запуск
app.run_polling(drop_pending_updates=True, allowed_updates=Update.ALL_TYPES)
