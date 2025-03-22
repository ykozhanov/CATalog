from typing import Any, Generator, TypeVar, ContextManager

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.db_lib.base.session import DBSessionCRUDInterface, DBSessionWhereInterface, DBSessionREInterface
from src.db_lib.base.exceptions import NotFoundInDBError, BadRequestDBError, IntegrityDBError
from src.db_lib.base.exceptions.messages import MESSAGE_BAD_REQUEST_DB

T = TypeVar("T")


class SQLAlchemySession(DBSessionCRUDInterface, DBSessionWhereInterface, DBSessionREInterface):

    def __init__(self, session_generator: Generator[Session, None, None], autocommit: bool = False):
        self._session_generator = session_generator
        self._autocommit = autocommit

    def create(self, obj: T) -> T:
        with self._session_generator() as session:
            try:
                session.add(obj)
                if not self._autocommit:
                    return obj
                session.commit()
                session.refresh(obj)
                return obj
            except IntegrityError:
                session.rollback()
                raise IntegrityDBError()
            except Exception as e:
                session.rollback()
                raise e

    def read(self, model: type[T], pk: int | str | tuple) -> T | None:
        with self._session_generator() as session:
            try:
                return session.get(model, pk)
            except Exception as e:
                session.rollback()
                raise e

    def update(self, model: type[T], obj_data: dict[str, Any], pk: int | str | tuple) -> T:
        with self._session_generator() as session:
            try:
                obj = session.get(model, pk)
                if obj is None:
                    raise NotFoundInDBError()
                for key, value in obj_data.items():
                    setattr(obj, key, value)
                if self._autocommit:
                    session.commit()
                return session.get(model, pk)
            except Exception as e:
                session.rollback()
                raise e

    def delete(self, model: type[T], pk: int | str | tuple) -> None:
        with self._session_generator() as session:
            try:
                obj = self.read(model=model, pk=pk)
                if obj is None:
                    raise NotFoundInDBError()
                session.delete(obj)
                if self._autocommit:
                    session.commit()
            except Exception as e:
                session.rollback()
                raise e

    def read_all(self, model: type[T], order_by: str | None = None) -> list[T]:
        with self._session_generator() as session:
            try:
                if order_by is None:
                    return session.query(model).all()
                return session.query(model).order_by(order_by).all()
            except Exception as e:
                session.rollback()
                raise e

    def where(self, model: type[T], attr: str, content: Any) -> list[T]:
        with self._session_generator() as session:
            try:
                return session.query(model).filter(getattr(model, attr) == content).all()
            except Exception as e:
                session.rollback()
                raise e

    def re(self, model: type[T], main_attr: str, filters: dict[str, Any], pattern: str) -> list[T]:
        with self._session_generator() as session:
            main_attr_data = filters.get(main_attr)
            if not isinstance(main_attr_data, str):
                raise BadRequestDBError(f"{MESSAGE_BAD_REQUEST_DB}: значение 'main_attr' в 'filters' должно быть str")
            try:
                query = session.query(model).filter(getattr(model, main_attr_data).op("~*")(pattern))
                for attr, value in filters.items():
                    if attr != main_attr:
                        query = query.filter(getattr(model, attr) == value)
                return query.all()
            except Exception as e:
                session.rollback()
                raise e

    def session(self) -> Session:
        with self._session_generator() as session:
            return session
