from typing import Callable

from pydantic import BaseModel, ConfigDict
from celery import Task
from celery.schedules import crontab


class PeriodicTask(BaseModel):
    schedule: crontab
    task: Callable[..., Task]
    name: str
    args: list = []
    kwargs: dict = {}
    expires: int | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
