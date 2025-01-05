from abc import ABC, abstractmethod
from typing import Type, TypeVar, Any

from .session import DatabaseSessionInterface, WhereSessionInterface

T = TypeVar("T")


class CRUDInterface(ABC):

    @abstractmethod
    def create(self, obj: T) -> T:
        pass

    @abstractmethod
    def read(self, model: Type[T], pk: int) -> T | None:
        pass

    @abstractmethod
    def update(self, model: Type[T], pk: int, obj_data: dict) -> T:
        pass

    @abstractmethod
    def delete(self, model: Type[T], pk: int) -> None:
        pass

    @abstractmethod
    def read_all(self, model: Type[T]) -> list[T]:
        pass


class CRUDWhereInterface(CRUDInterface):

    @abstractmethod
    def where(self, model: Type[T], attr: str, content: Any) -> list[T]:
        pass


class CRUDBase(CRUDInterface):

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


class CRUDMax(CRUDBase, CRUDWhereInterface):

    def __init__(self, session: WhereSessionInterface):
        super().__init__(session=session)
        self._where_session = session

    def where(self, model: Type[T], attr: str, content: Any) -> list[T]:
        return self._where_session.where(model=model, attr=attr, content=content)
