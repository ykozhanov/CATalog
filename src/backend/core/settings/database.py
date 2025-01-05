from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session as SessionType

from src.backend.settings import DB_PATH
from ..db_lib.sqlalchemy import SQLAlchemySession
from ..db_lib.base import CRUD

engine = create_engine(DB_PATH)

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


def get_session() -> Generator[SessionType, None, None]:
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


crud = CRUD(session=SQLAlchemySession(session_generator=get_session()))
