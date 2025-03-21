from celery.schedules import crontab

from src.notification_service.core.celery_config.schemas import PeriodicTask

from src.notification_service.telegram.settings import settings
from src.notification_service.telegram.tasks.task_notification_exp_products import push_notification_telegram_exp_products

notification_exp_products_periodic_task = PeriodicTask(
    schedule=crontab(hour=settings.notification_hour_utc, minute=settings.notification_minutes_utc),
    task=push_notification_telegram_exp_products,
    name="push_notification_telegram_exp_products",
)

beats_telegram: list[PeriodicTask] = [
    notification_exp_products_periodic_task,
]
