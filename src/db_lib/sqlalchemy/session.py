from typing import Type, Any, Generator, Optional, TypeVar
from sqlalchemy.orm import Session

from src.db_lib.base.session import DBSessionCRUDInterface, DBSessionWhereInterface, DBSessionREInterface
from src.db_lib.base.exceptions import NotFoundInDBError

T = TypeVar("T")
OB = TypeVar("OB")


class SQLAlchemySession(DBSessionCRUDInterface, DBSessionWhereInterface, DBSessionREInterface):

    def __init__(self, session_generator: Generator[Session, None, None], autocommit: Optional[bool] = False):
        self._session_generator = session_generator
        self._autocommit = autocommit

    def create(self, obj: T) -> T:
        with next(self._session_generator) as session:
            session.add(obj)
            if not self._autocommit:
                session.commit()
            session.refresh(obj)
            return obj

    def read(self, model: Type[T], pk: int) -> T | None:
        with next(self._session_generator) as session:
            return session.query(model).get(pk)

    def update(self, model: Type[T], obj_data: dict[str, Any], pk: int) -> T:
        with next(self._session_generator) as session:
            obj = session.query(model).get(pk)
            if obj is None:
                raise NotFoundInDBError()
            for key, value in obj_data.items():
                setattr(obj, key, value)
            if not self._autocommit:
                session.commit()
            return obj

    def delete(self, model: Type[T], pk: int) -> None:
        with next(self._session_generator) as session:
            obj = self.read(model=model, pk=pk)
            if obj is None:
                raise NotFoundInDBError()
            session.delete(obj)
            if not self._autocommit:
                session.commit()

    def read_all(self, model: Type[T], order_by: OB | None) -> list[T]:
        with next(self._session_generator) as session:
            if order_by is None:
                return session.query(model).all()
            return session.query(model).order_by(order_by).all()


    def delete_all(self, model: Type[T], attr: str, for_delete: Any) -> None:
        with next(self._session_generator) as session:
            session.query(model).filter(getattr(model, attr) == for_delete).delete(synchronize_session='fetch')
            if not self._autocommit:
                session.commit()

    def where(self, model: Type[T], attr: str, search: Any) -> list[T]:
        with next(self._session_generator) as session:
            return session.query(model).filter(getattr(model, attr) == search).all()

    def re(self, model: Type[T], attr: str, pattern: str) -> list[T]:
        with next(self._session_generator) as session:
            return session.query(model).filter(getattr(model, attr).op("REGEXP")(pattern)).all()
