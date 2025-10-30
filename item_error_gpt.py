import logging
from telegram.error import Conflict, NetworkError

logger = logging.getLogger(__name__)

async def error_gpt(update, context):
    logger.error(f"Помилка під час обробки оновлення: {context.error}")
    if isinstance(context.error, Conflict):
        logger.error("Конфлікт: інший екземпляр бота вже запущено.")
    elif isinstance(context.error, NetworkError):
        logger.error(f"Помилка мережі: {context.error}")