from abc import ABC, abstractmethod
from typing import TypeVar, Any

from .session import DBSessionCRUDInterface, DBSessionWhereInterface, DBSessionREInterface

T = TypeVar("T")


class DBControllerCRUDInterface(ABC):

    @abstractmethod
    def create(self, obj: T) -> T:
        pass

    @abstractmethod
    def read(self, model: type[T], pk: int | str) -> T | None:
        pass

    @abstractmethod
    def update(self, model: type[T], pk: int | str, obj_data: dict) -> T:
        pass

    @abstractmethod
    def delete(self, model: type[T], pk: int | str) -> None:
        pass

    @abstractmethod
    def read_all(self, model: type[T], order_by: str | None) -> list[T]:
        pass


class DBControllerWhereInterface(ABC):

    @abstractmethod
    def where(self, model: type[T], attr: str, content: Any) -> list[T]:
        pass


class DBControllerREInterface(ABC):

    @abstractmethod
    def re(self, model: type[T], main_attr: str, filters: dict[str, Any], pattern: str) -> list[T]:
        pass


class DBControllerCRUD(DBControllerCRUDInterface):

    def __init__(self, session_crud: DBSessionCRUDInterface):
        self._session_crud = session_crud

    def create(self, obj: T) -> T:
        new_obj = self._session_crud.create(obj=obj)
        return new_obj

    def read(self, model: type[T], pk: int | str) -> T | None:
        return self._session_crud.read(model=model, pk=pk)

    def update(self, model: type[T], pk: int | str, obj_data: dict) -> T:
        return self._session_crud.update(model=model, obj_data=obj_data, pk=pk)

    def delete(self, model: type[T], pk: int | str) -> None:
        self._session_crud.delete(model=model, pk=pk)

    def read_all(self, model: type[T], order_by: str | None = None) -> list[T]:
        return self._session_crud.read_all(model=model, order_by=order_by)


class DBControllerWhere(DBControllerWhereInterface):

    def __init__(self, session_where: DBSessionWhereInterface):
        self._session_where = session_where

    def where(self, model: type[T], attr: str, content: Any) -> list[T]:
        return self._session_where.where(model=model, attr=attr, content=content)


class DBControllerRE(DBControllerREInterface):

    def __init__(self, session_re: DBSessionREInterface):
        self._session_re = session_re

    def re(self, model: type[T], main_attr: str, filters: dict[str, Any], pattern: str) -> list[T]:
        return self._session_re.re(model=model, main_attr=main_attr, filters=filters, pattern=pattern)


class DBControllerMax(DBControllerWhere, DBControllerCRUD, DBControllerRE):

    def __init__(self, session_crud: DBSessionCRUDInterface, session_where: DBSessionWhereInterface, session_re: DBSessionREInterface):
        DBControllerCRUD.__init__(self, session_crud)
        DBControllerWhere.__init__(self, session_where)
        DBControllerRE.__init__(self, session_re)
