from typing import Callable

from pydantic import BaseModel
from celery.schedules import crontab


class PeriodicTask(BaseModel):
    schedule: crontab
    task: Callable
    name: str
    args: list = []
    kwargs: dict = {}
    expires: int | None = None

    class Config:
        arbitrary_types_allowed = True

