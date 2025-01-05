from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session as SessionType, declarative_base

from src.db_lib.sqlalchemy import SQLAlchemySession
from src.db_lib.base import CRUDMax
from src.backend.settings import DB_PATH

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


crud = CRUDMax(session=SQLAlchemySession(session_generator=get_session()))

Base = declarative_base()
