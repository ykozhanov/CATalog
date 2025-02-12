from typing import Generator

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session as SessionType

from src.backend.settings import get_db_path
from src.backend.core.settings_app import redis_cache_url

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
    finally:
        session.close()

redis_cache = redis.from_url(redis_cache_url())
