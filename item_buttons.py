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
TALK_CONTINUE_BUTTONS = {
    'talk_change': 'Вибрати іншу особистість',
    'start': 'Закінчити'
}

#Кнопки для квізу
QUIZ_BUTTONS = {
    'topic_history': 'Історія',
    'topic_science': 'Наука',
    'topic_movies': 'Кіно',
    'topic_music': 'Музика',
    'topic_tech': 'Технології'
}

#Кнопки піля відповіді
QUIZ_ACTION_BUTTONS = {
    'quiz_next': 'Наступне питання',
    'quiz_change':'Змінити тему',
    'quiz_end':'Завершити квіз'
}

# Кнопка виходу в меню
QUIZ_EXIT_BUTTONS = {
    'start': 'Закінчити'
}
# Кнопки мов
LANG_BUTTONS = {
    'lang_en': 'Англійська',
    'lang_es': 'Іспанська',
    'lang_fr': 'Французька',
    'lang_de': 'Німецька',
    'start': 'Закінчити'
}

# Кнопки після перекладу
TRANSLATE_CONTINUE_BUTTONS = {
    'translator_change': 'Змінити мову',
    'start': 'Закінчити'
}

# функція для створення клавіатури
def get_keyboard(buttons_dict):
    keyboard = [
        [InlineKeyboardButton(text, callback_data=key)]
        for key, text in buttons_dict.items()
    ]
    return InlineKeyboardMarkup(keyboard)