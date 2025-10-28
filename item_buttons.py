from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# словники кнопок
RANDOM_BUTTONS = {
    'random': 'Хочу ще факт',
    'start': 'Закінчити'
}

QUESTION_BUTTONS = {
    'start': 'Закінчити'
}

MAIN_MENU_BUTTONS = {
    'start': 'Головне меню',
    'random': 'Дізнатися випадковий факт',
    'gpt': 'Задати питання ChatGPT',
    'talk': 'Поговорити з відомою особистістю',
    'quiz': 'Взяти участь у квізі',
    'translator': 'Переклад слів'
}

# функція для створення клавіатури
def get_keyboard(buttons_dict):
    keyboard = [
        [InlineKeyboardButton(text, callback_data=key)]
        for key, text in buttons_dict.items()
    ]
    return InlineKeyboardMarkup(keyboard)