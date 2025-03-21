import logging

from celery import shared_task, Task

from src.notification_service.telegram.database import TelegramUserController
from src.notification_service.telegram.api import UsersAPI, ProductsAPI
from src.notification_service.telegram.api.products.schemas import ProductInSchema
from src.notification_service.telegram.bot import bot


def get_access_token(refresh_token: str) -> str | None:
    logging.info(f"Старт 'get_access_token'")
    logging.debug(f"refresh_token: {refresh_token}")
    try:
        user_data = UsersAPI.token(refresh_token)
        logging.info(f"Конец 'get_access_token'")
        return user_data.access_token
    except Exception as e:
        logging.error(e)
        logging.info(f"Конец 'get_access_token'")


def get_products(access_token: str) -> list[ProductInSchema] | None:
    logging.info(f"Старт 'get_products'")
    try:
        p_api = ProductsAPI(access_token)
        logging.info(f"Конец 'get_products'")
        return p_api.get_by()
    except Exception as e:
        logging.error(e)
        logging.info(f"Конец 'get_products'")


@shared_task
def push_notification_telegram_exp_products() -> Task:
    logging.info(f"Старт 'push_notification_telegram_exp_products'")
    users = TelegramUserController.read_all()
    for user in users:
        logging.debug(f"user: {user}")
        logging.debug(f"user.refresh_jtw_token: {user.refresh_jtw_token}")
        if a_token := get_access_token(user.refresh_jtw_token):
            if products := get_products(a_token):
                bot.send_message(
                    chat_id=user.telegram_chat_id,
                    text="Список продуктов у которых скоро заканчивается срок годности: {}."
                    .format(", ".join(p.name for p in products)),
                )
    logging.info(f"Конец 'push_notification_telegram_exp_products'")

