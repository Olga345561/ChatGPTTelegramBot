from telegram import Update
from telegram.ext import ContextTypes
from util import send_image, send_text, show_main_menu
from item_buttons import MAIN_MENU_BUTTONS
from util import load_message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, MAIN_MENU_BUTTONS)


