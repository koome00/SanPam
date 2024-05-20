"""
 Users and Files tables
"""
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String
from datetime import datetime

DATA = {}
class Base(DeclarativeBase):
    """
    declarative base
    """
    pass

class User(Base):
    __tablename__ = "user_account"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(30), nullable=False)
    email = mapped_column(String, nullable=False)
    hashed_password = mapped_column(String, nullable=False)
    created_at = mapped_column(String, nullable=False, default=datetime.utcnow)
    role = mapped_column(String, nullable=True)
    session_id = mapped_column(String, nullable=False)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"
    
    
