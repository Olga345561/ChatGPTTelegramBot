from telegram import InlineKeyboardButton, InlineKeyboardMarkup

MAIN_MENU_BUTTONS = {
    'start': 'Головне меню',
    'random': 'Дізнатися випадковий факт',
    'gpt': 'Задати питання ChatGPT',
    'talk': 'Поговорити з відомою особистістю',
    'quiz': 'Взяти участь у квізі',
    'translator': 'Переклад слів'
}
# словники кнопок
RANDOM_BUTTONS = {
    'random': 'Хочу ще факт',
    'start': 'Закінчити'
}

# словник до кнопки "Закінчити" у item_question
QUESTION_BUTTONS = {
    'start': 'Закінчити'
}

#словник кнопок для відомих особистостей з talk
PERSON_BUTTONS = {
    'talk_usyk': 'Олександр Усик',
    'talk_zelenskyi': 'Володимир Зеленський',
    'talk_queen':'Королева Єлизавета II',
    'talk_dragons': 'Ден Рейнольдс',
    'talk_einstein': 'Альберт Енштейн',
    'start': 'Закінчити'
}

# функція для створення клавіатури
def get_keyboard(buttons_dict):
    keyboard = [
        [InlineKeyboardButton(text, callback_data=key)]
        for key, text in buttons_dict.items()
    ]
    return InlineKeyboardMarkup(keyboard)