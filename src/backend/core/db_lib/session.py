from typing import TypeVar, Type, Any
from abc import ABC, abstractmethod

T = TypeVar("T")


class DatabaseSessionInterface(ABC):

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
    def list_all(self, model: Type[T]) -> list[T]:
        pass
