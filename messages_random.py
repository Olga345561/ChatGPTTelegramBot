from telegram import Update
from telegram.ext import ContextTypes
from util import (send_text, load_prompt, send_image, send_text_buttons)
from menu_handler import start
from item_random import random_fact
from item_qpt import gpt_handler
from item_talk import talk_handler


# Окремий обробник для інтерпретації випадкових повідомлень користувача
async def interpret_random_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()

    if any(keyword in message_text for keyword in ['факт', 'цікав', 'random', 'випадков']):
        await send_text(update, context, "🧠 Схоже, ви цікавитесь випадковими фактами! Зараз покажу вам один...")
        await random_fact(update, context)
        return True

    elif any(keyword in message_text for keyword in ['gpt', 'чат', 'питання', 'запита', 'дізнатися']):
        await send_text(update, context, "🤖 Схоже, у вас є питання! Переходимо до режиму спілкування з ChatGPT...")
        await gpt_handler(update, context)
        return True

    elif any(keyword in message_text for keyword in ['розмов', 'говори', 'спілкува', 'особист', 'talk']):
        await send_text(update, context, "👤 Схоже, ви хочете поговорити з відомою особистістю! Зараз покажу вам доступні варіанти...")
        await talk_handler(update, context)
        return True

    return False

# Обробник для відображення кумедної відповіді, коли намір не визначено
async def show_funny_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показує випадкову кумедну відповідь, коли не вдається визначити намір користувача."""
    import random

    # Випадкові кумедні відповіді, якщо наміри не визначені
    funny_responses = [
        "🤔 Хмм... Цікаво, але я не зрозумів, що саме ви хочете. Може спробуєте одну з команд з меню?",
        "🧐 Дуже цікаве повідомлення! Але мені потрібні чіткіші інструкції. Ось доступні команди:",
        "😅 Ой, здається, ви мене застали зненацька! Я вмію багато чого, але мені потрібна конкретна команда:",
        "🤖 *перезавантажується* Вибачте, мої алгоритми не розпізнали це як команду. Ось що я точно вмію:",
        "🦄 Це повідомлення таке ж загадкове, як єдиноріг у дикій природі! Спробуйте одну з цих команд:",
        "🕵️ Я намагаюся зрозуміти ваше повідомлення... Але краще скористайтесь однією з команд:",
        "🎲 О! Випадкове повідомлення! Я теж вмію бути випадковим, але краще використовуйте команди:",
        "📱 *натискає уявні кнопки* Гм, не спрацювало. Може спробуємо ці команди?",
        "🌈 Це повідомлення прекрасне, як веселка! Але для повноцінного спілкування спробуйте:",
        "🤓 Згідно з моїми розрахунками, це повідомлення не відповідає жодній з моїх команд. Ось вони:",
    ]

    # Додаткові підказки для покращення взаємодії
    hints = [
        "Спробуйте команду /gpt, щоб задати питання",
        "Використайте /random для отримання цікавого факту",
        "Команда /talk дозволить вам поспілкуватися з відомою особистістю",
        "Не знаєте, що обрати? Почніть з /start",
    ]

    # Формуємо повідомлення з кумедною відповіддю та підказкою
    response = f"{random.choice(funny_responses)}\n\n💡 *Підказка:* {random.choice(hints)}"
    await send_text(update, context, response)

    # Показуємо основне меню
    await start(update, context)


