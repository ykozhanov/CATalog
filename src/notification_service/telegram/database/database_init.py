from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session as SessionType

from src.notification_service.telegram.settings import get_db_path

engine = create_engine(get_db_path())

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


def get_session() -> Generator[SessionType, None, None]:
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
