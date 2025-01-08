from typing import TypeVar, Type, Any
from abc import ABC, abstractmethod

T = TypeVar("T")
OB = TypeVar("OB")


class DBSessionCRUDInterface(ABC):

    @abstractmethod
    def create(self, obj: T) -> T:
        pass

    @abstractmethod
    def read(self, model: Type[T], pk: int) -> T | None:
        pass

    @abstractmethod
    def update(self, model: Type[T], obj_data: dict[str, Any], pk: int) -> T:
        pass

    @abstractmethod
    def delete(self, model: Type, pk: int) -> None:
        pass

    @abstractmethod
    def read_all(self, model: Type[T], order_by: OB | None) -> list[T]:
        pass

    @abstractmethod
    def delete_all(self, model: Type[T], attr: str, for_delete: Any) -> None:
        pass


class DBSessionWhereInterface(ABC):

    @abstractmethod
    def where(self, model: Type[T], attr: str, content: Any) -> list[T]:
        pass


class DBSessionREInterface(ABC):

    @abstractmethod
    def re(self, model: Type[T], attr: str, pattern: str) -> list[T]:
        pass


# class DBSessionCRUDWhereInterface(DBSessionCRUDInterface, DBSessionWhereInterface, ABC):
#     pass
