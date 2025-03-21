from celery import Celery

from src.notification_service.core.settings import settings

if settings.debug:
    import logging
    logging.basicConfig(
        level=logging.DEBUG,  # Уровень логирования
        format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщения
        handlers=[
            logging.StreamHandler(),  # Вывод в консоль
        ]
    )

from src.notification_service.core.celery_config.schemas import PeriodicTask
from src.notification_service.telegram.beats import beats_telegram

app = Celery("celery", broker=settings.redis_url())

app.autodiscover_tasks(["src.notification_service.telegram.tasks"])

all_beats: list[PeriodicTask] = [
    *beats_telegram,
]


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    logging.info(f"Старт 'setup_periodic_tasks'")
    for b in all_beats:
        logging.debug(f"beat: {b}")
        sender.add_periodic_task(
            b.schedule,
            b.task.s(*b.args, **b.kwargs),
            name=b.name,
            expires=b.expires,
        )
    logging.info(f"Конец 'setup_periodic_tasks'")
