from celery import Celery

from pytz import timezone

from src.notification_service.core.settings import Settings
from src.notification_service.core.celery_config.schemas import PeriodicTask

from src.notification_service.telegram.beats import beats_telegram

app = Celery("celery", broker=Settings.redis_url_notification_service)

app.autodiscover_tasks(["src.notification_service.telegram.tasks"])

all_beats: list[PeriodicTask] = [
    *beats_telegram,
]


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    for b in all_beats:
        sender.add_periodic_task(
            b.schedule,
            b.task(*b.args, **b.kwargs),
            name=b.name,
            expires=b.expires,
        )

app.conf.timezone = "UTC"
