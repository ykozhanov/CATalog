from typing import TypeVar, Any
from abc import ABC, abstractmethod

T = TypeVar("T")


class DBSessionCRUDInterface(ABC):

    @abstractmethod
    def create(self, obj: T) -> T:
        pass

    @abstractmethod
    def read(self, model: type[T], pk: int | str) -> T | None:
        pass

    @abstractmethod
    def update(self, model: type[T], obj_data: dict[str, Any], pk: int | str) -> T:
        pass

    @abstractmethod
    def delete(self, model: type, pk: int | str) -> None:
        pass

    @abstractmethod
    def read_all(self, model: type[T], order_by: str | None = None) -> list[T]:
        pass

    @abstractmethod
    def delete_all(self, model: type[T], attr: str, for_delete: Any) -> None:
        pass


class DBSessionWhereInterface(ABC):

    @abstractmethod
    def where(self, model: type[T], attr: str, content: Any) -> list[T]:
        pass


class DBSessionREInterface(ABC):

    @abstractmethod
    def re(self, model: type[T], attr: str, pattern: str) -> list[T]:
        pass
