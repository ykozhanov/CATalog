from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import Mapper

from .base import Base


class User(Base):
    id: Mapper[int] = Column(Integer, primary_key=True)
    username: Mapper[str] = Column(String(length=100), unique=True)
    password: Mapper[bytes] = Column(LargeBinary, nullable=False)
    email: Mapper[str] = Column(String(length=150), nullable=False)
