"""
 Users and Files tables
"""
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import Integer, String
from datetime import datetime

DATA = {}
time = "%Y-%m-%dT%H:%M:%S.%f"
class Base(DeclarativeBase):
    """
    declarative base
    """
    pass

class User(Base):
    __tablename__ = "user_account"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String(30))
    email = mapped_column(String, nullable=False, unique=True)
    hashed_password = mapped_column(String, nullable=False)
    created_at = mapped_column(String, nullable=False, default=datetime.utcnow)
    role = mapped_column(String)
    session_id = mapped_column(String)
    reset_token = mapped_column(String)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.__dict__}"
    

    def to_dict(self):
        DATA = self.__dict__.copy()
        return DATA
