import os
from typing import Generator
from contextlib import contextmanager

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session as SessionType

from src.backend.core.exceptions import ENVError
from src.backend.core.exceptions.messages import MESSAGE_ENV_ERROR


def get_db_path(host: str | None = None, port: str | int | None = None) -> str:
    return "postgresql://{username}:{password}@{host}:{port}/{dbname}".format(
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=host if host else os.getenv("POSTGRES_HOST"),
        port=port if port else os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("DB_NAME_BACKEND"),
    )

engine = create_engine(get_db_path())

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


@contextmanager
def get_session() -> Generator[SessionType, None, None]:
    session = Session()
    try:
        yield Session()
    finally:
        session.close()


REDIS_HOSTNAME_CACHE_B = os.getenv("REDIS_HOSTNAME")
REDIS_PORT_CACHE_B = os.getenv("REDIS_PORT")
REDIS_DB_CACHE_B = os.getenv("REDIS_DB")
REDIS_PASSWORD_CACHE_B = os.getenv("REDIS_PASSWORD")


def redis_cache_url() -> str:
    if not REDIS_HOSTNAME_CACHE_B or not REDIS_PORT_CACHE_B or not REDIS_DB_CACHE_B:
        raise ENVError(f"{MESSAGE_ENV_ERROR}: установите REDIS_HOSTNAME_CACHE_B, REDIS_PORT_CACHE_B и REDIS_PASSWORD_CACHE_B")
    if REDIS_PASSWORD_CACHE_B is not None:
        return f"redis://:{REDIS_PASSWORD_CACHE_B}@{REDIS_HOSTNAME_CACHE_B}:{REDIS_PORT_CACHE_B}/{REDIS_DB_CACHE_B}"
    return f"redis://{REDIS_HOSTNAME_CACHE_B}:{REDIS_PORT_CACHE_B}/{REDIS_DB_CACHE_B}"


redis_cache = redis.from_url(redis_cache_url())
