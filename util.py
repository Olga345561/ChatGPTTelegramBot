from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Message, \
    BotCommand, MenuButtonCommands, BotCommandScopeChat, MenuButtonDefault
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CallbackContext


#завантажує повідомлення з папки resources/ messages/
def load_message(name):
    with open("resources/messages/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()

#надсилає фото в чат
async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE,
                     name: str) -> Message:
    with open(f'resources/images/{name}.jpg', 'rb') as image:
        return await context.bot.send_photo(chat_id=update.effective_chat.id,
                                            photo=image)

#надсилає в чат текстові повідомлення
async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE,
                    text:str) ->Message:
    if text.count('_') % 2 !=0:
        message = f"Рядок '{text}' є невалідним з точки зору makdown. Скористайтесь методом send_html()"
        print(message)
        return await update.message.reply_text(message)

    text = text.encode('utf16', errors='surrogatepass').decode('utf16')
    return await context.bot.send_message(chat_id=update.effective_chat.id,
                                          text=text,
                                          parse_mode=ParseMode.MARKDOWN)

#відображає команду та головне меню
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE,
                         commands: dict):
    command_list = [BotCommand(key, value) for key, value in commands.items()]
    await context.bot.set_my_commands(command_list, scope=BotCommandScopeChat(
        chat_id=update.effective_chat.id))
    await context.bot.set_chat_menu_button(menu_button=MenuButtonCommands(),
                                           chat_id=update.effective_chat.id)

#конвертує об'єкт ser в рядок
def dialog_user_info_to_str(user_data):
    mapper = {'language_form': 'Мова оригіналу', 'language_to': 'Мова перекладу',
              'text_to_translate': 'Текст для перекладу'}
    return '\n'.join(map(lambda k,v: (mapper[k], v), user_data.items()))

#надсилає в чат текстове повідомлення
async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE,
                    text:str) ->Message:
    if text.count('_') % 2 !=0:
        message = f"Рядок '{text}' є невалідним з точки зору markdown. користайтесь методом send_html()"
        print(message)
        return await update.message.reply_text(message)
    text = text.encode('utf16', errors='surrogatepass').decode('utf16')
    return await context.bot.send_message(chat_id=update.effective_chat.id,
                                          text=text,
                                          parse_mode=ParseMode.MARKDOWN)

# завантажує промпт з папки /resources/messages/
def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()

# надсилає в чат текстове повідомлення, та додає до нього кнопки
async def send_text_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE,
                            text:str, buttons:dict) ->Message:
    text = text.encode('utf16', errors='surrogatepass').decode('utf16')
    keyboard = []
    for key, value in buttons.items():
        button = InlineKeyboardButton(str(value), callback_data=str(key))
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return await context.bot.send_message(
        update.effective_message.chat.id,
        text=text, reply_markup=reply_markup,
        message_thread_id=update.effective_message.message_thread_id)
