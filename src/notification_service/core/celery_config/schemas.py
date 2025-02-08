from datetime import timedelta

from pydantic import BaseModel
from celery import Task


class PeriodicTask(BaseModel):
    interval: timedelta
    task: Task
    name: str
    args: list = []
    kwargs: dict = {}
    expires: int | None = None
