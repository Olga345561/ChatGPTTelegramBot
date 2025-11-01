import logging
from telegram.error import Conflict, NetworkError
from util import send_text  # якщо є твоя функція для надсилання повідомлень

logger = logging.getLogger(__name__)

async def error_gpt(update, context):
    logger.error(f"Помилка під час обробки оновлення: {context.error}")

    if isinstance(context.error, Conflict):
        logger.error("Конфлікт: інший екземпляр бота вже запущено.")
    elif isinstance(context.error, NetworkError):
        logger.error(f"Помилка мережі: {context.error}")

    # Відправка повідомлення користувачу про помилку
    try:
        await send_text(update, context, "😔 Виникла помилка. Спробуйте ще раз пізніше.")
    except Exception as e:
        logger.warning(f"Не вдалося надіслати повідомлення про помилку: {e}")
