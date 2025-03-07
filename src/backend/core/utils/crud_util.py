from src.db_lib.sqlalchemy import SQLAlchemySession
from src.db_lib.base import DBControllerMax

from src.backend.core.database.database_init import get_session

session = SQLAlchemySession(session_generator=get_session, autocommit=True)
crud = DBControllerMax(session_crud=session, session_where=session, session_re=session)
