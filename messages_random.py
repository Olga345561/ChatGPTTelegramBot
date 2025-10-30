from telegram import Update
from telegram.ext import ContextTypes
from util import send_text
import random
from menu_handler import start  # якщо menu_handler імпортує messages_random — зроби локальний імпорт в show_funny_response (див. нижче)

async def interpret_random_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Аналізує текст повідомлення і виконує відповідну дію.
    Повертає True, якщо оброблено (виконана дія), і False якщо не вдалося визначити намір.
    """
    # Захист від апдейтів без тексту
    if not update.message or not update.message.text:
        return False

    message_text = update.message.text.lower().strip()

    # Перевірка на випадкові факти
    if any(keyword in message_text for keyword in ['факт', 'цікав', 'random', 'випадков']):
        # Локальний імпорт, щоб уникнути циклічних залежностей на рівні модуля
        from item_random import random_fact
        await send_text(update, context, "🧠 Схоже, ви цікавитесь випадковими фактами! Зараз покажу вам один...")
        await random_fact(update, context)
        return True

    # Переходи в режим ChatGPT
    if any(keyword in message_text for keyword in ['gpt', 'чат', 'питання', 'запита', 'дізнатися']):
        from item_question import gpt_handler
        await send_text(update, context, "🤖 Схоже, у вас є питання! Переходимо до режиму спілкування з ChatGPT...")
        await gpt_handler(update, context)
        return True

    # Перехід у режим talk
    if any(keyword in message_text for keyword in ['розмов', 'говори', 'спілкува', 'особист', 'talk']):
        # Локальний імпорт item_talk щоб уникнути циклічності при імпорті модулів
        from item_talk import talk_handler
        await send_text(update, context, "👤 Схоже, ви хочете поговорити з відомою особистістю! Зараз покажу вам доступні варіанти...")
        await talk_handler(update, context)
        return True

    return False


async def show_funny_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показує випадкову кумедну відповідь, коли намір не визначено."""
    funny_responses = [
        "🤔 Хмм... Цікаво, але я не зрозумів, що саме ви хочете. Може спробуєте одну з команд з меню?",
        "🧐 Дуже цікаве повідомлення! Але мені потрібні чіткіші інструкції. Ось доступні команди:",
        "😅 Ой, здається, ви мене застали зненацька! Я вмію багато чого, але мені потрібна конкретна команда:",
        "🤖 *перезавантажується* Вибачте, мої алгоритми не розпізнали це як команду. Ось що я точно вмію:",
        "🦄 Це повідомлення таке ж загадкове, як єдиноріг у дикій природі! Спробуйте одну з цих команд:",
    ]

    hints = [
        "Спробуйте команду /gpt, щоб задати питання",
        "Використайте /random для отримання цікавого факту",
        "Команда /talk дозволить вам поспілкуватися з відомою особистістю",
        "Не знаєте, що обрати? Почніть з /start",
    ]

    response = f"{random.choice(funny_responses)}\n\n💡 *Підказка:* {random.choice(hints)}"
    await send_text(update, context, response)

    # локальний імпорт start (щоб уникнути циклічних імпортів, якщо menu_handler імпортує messages_random)
    try:
        from menu_handler import start as menu_start
        # показувати меню не завжди — тут показуємо завжди; можеш обмежити ймовірність
        await menu_start(update, context)
    except Exception:
        # якщо не можна імпортувати, просто пропускаємо (щоб не падати)
        pass
