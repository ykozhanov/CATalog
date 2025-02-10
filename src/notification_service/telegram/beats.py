from celery.schedules import crontab
from pytz import utc

from src.notification_service.core.celery_config.schemas import PeriodicTask

from src.notification_service.telegram.tasks.task_notification_exp_products import push_notification_telegram_exp_products

notification_exp_products_periodic_task = PeriodicTask(
    schedule=crontab(hour="14", minute="0", tz=utc),    # 19:00 по Екатеринбургу
    task=push_notification_telegram_exp_products,
    name="push_notification_telegram_exp_products",
)

beats_telegram: list[PeriodicTask] = [
    notification_exp_products_periodic_task,
]
