from src.db_lib.sqlalchemy import SQLAlchemySession
from src.db_lib.base import DBControllerMax

from src.notification_service.telegram.database.database_init import get_session

session = SQLAlchemySession(session_generator=get_session())
crud = DBControllerMax(session_crud=session, session_where=session, session_re=session)
