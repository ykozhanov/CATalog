from typing import Any, Generator, TypeVar
from sqlalchemy.orm import Session

from src.db_lib.base.session import DBSessionCRUDInterface, DBSessionWhereInterface, DBSessionREInterface
from src.db_lib.base.exceptions import NotFoundInDBError

T = TypeVar("T")


class SQLAlchemySession(DBSessionCRUDInterface, DBSessionWhereInterface, DBSessionREInterface):

    def __init__(self, session_generator: Generator[Session, None, None], autocommit: bool = False):
        self._session_generator = session_generator
        self._autocommit = autocommit

    def create(self, obj: T) -> T:
        with next(self._session_generator) as session:
            session.add(obj)
            if self._autocommit:
                session.commit()
            session.refresh(obj)
            return obj

    def read(self, model: type[T], pk: int | str) -> T | None:
        with next(self._session_generator) as session:
            return session.query(model).get(pk)

    def update(self, model: type[T], obj_data: dict[str, Any], pk: int | str) -> T:
        with next(self._session_generator) as session:
            obj = session.query(model).get(pk)
            if obj is None:
                raise NotFoundInDBError()
            for key, value in obj_data.items():
                setattr(obj, key, value)
            if self._autocommit:
                session.commit()
            return obj

    def delete(self, model: type[T], pk: int | str) -> None:
        with next(self._session_generator) as session:
            obj = self.read(model=model, pk=pk)
            if obj is None:
                raise NotFoundInDBError()
            session.delete(obj)
            if self._autocommit:
                session.commit()

    def read_all(self, model: type[T], order_by: str | None = None) -> list[T]:
        with next(self._session_generator) as session:
            if order_by is None:
                return session.query(model).all()
            return session.query(model).order_by(order_by).all()

    def where(self, model: type[T], attr: str, search: Any) -> list[T]:
        with next(self._session_generator) as session:
            return session.query(model).filter(getattr(model, attr) == search).all()

    def re(self, model: type[T], main_attr: str, filters: dict[str, Any], pattern: str) -> list[T]:
        with next(self._session_generator) as session:
            query = session.query(model).filter(getattr(model, filters.get(main_attr)).op("REGEXP")(pattern))
            for attr, value in filters.items():
                if attr != main_attr:
                    query.filter(getattr(model, attr) == value)
            return query.all()

    def session(self) -> Session:
        with next(self._session_generator) as session:
            return session
