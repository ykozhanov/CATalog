from celery import shared_task

from src.notification_service.telegram.database import TelegramUserController
from src.notification_service.telegram.api import UsersAPI, ProductsAPI
from src.notification_service.telegram.api.products.schemas import ProductInSchema
from src.notification_service.telegram.bot import bot


def get_access_token(refresh_token: str) -> str | None:
    try:
        user_data = UsersAPI.token(refresh_token)
    except Exception as e:
        print(str(e))
        return None
    else:
        return user_data.access_token


def get_products(access_token: str) -> list[ProductInSchema] | None:
    try:
        p_api = ProductsAPI(access_token)
        return p_api.get_by()
    except Exception as e:
        print(str(e))
        return None


@shared_task
def push_notification_telegram_exp_products():
    users = TelegramUserController.read_all()
    for user in users:
        if a_token := get_access_token(user.refresh_jtw_token):
            if products := get_products(a_token):
                bot.send_message(
                    chat_id=user.telegram_chat_id,
                    text=f"""Список продуктов у которых скоро заканчивается срок годности:
                    \t{"\n\t".join(p.name for p in products)}
                    """
                )
