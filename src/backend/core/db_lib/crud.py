from typing import Type, TypeVar

from .session import DatabaseSessionInterface

T = TypeVar("T")


class CRUD:

    def __init__(self, session: DatabaseSessionInterface):
        self._session = session

    def create(self, obj: T) -> T:
        new_obj = self._session.create(obj=obj)
        return new_obj

    def read(self, model: Type[T], pk: int) -> T | None:
        return self._session.read(model=model, pk=pk)

    def update(self, model: Type[T], pk: int, obj_data: dict) -> T:
        return self._session.update(model=model, obj_data=obj_data, pk=pk)

    def delete(self, model: Type[T], pk: int) -> None:
        self._session.delete(model=model, pk=pk)

    def read_all(self, model: Type[T]) -> list[T]:
        return self._session.list_all(model=model)
