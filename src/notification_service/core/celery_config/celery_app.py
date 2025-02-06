from celery import Celery

from src.notification_service.core.settings import Settings

from src.notification_service.telegram.beats import beats

app = Celery("celery", broker=Settings.redis_url_notification_service)

app.autodiscover_tasks(["src.notification_service.telegram.tasks"])

all_beats: list[tuple] = [*beats]


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    for b in all_beats:
        sender.add_periodic_task(*b)