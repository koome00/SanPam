import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Optional, Union
from user import User


def _hash_password(password: str) -> bytes:
    """
    takes password and returns
    it hashed with bcrypt.hashpw
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"),
                           bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """
    generate uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        function to register user
        """
        try:
            if self._db.find_user(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hashed)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        credentials validation
        """
        try:
            user = self._db.find_user(email=email)
            if user:
                hashed = user.hashed_password
                return bcrypt.checkpw(password.encode(), hashed)
        except (InvalidRequestError, NoResultFound):
            return self._db.all()

    def create_session(self, email: str) -> Union[str, None]:
        """
        creates session ID and returns a string
        """
        try:
            user = self._db.find_user(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.email, session_id=session_id)
            return session_id
        except (NoResultFound, InvalidRequestError, ValueError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        takes session_id and returns user
        or none
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroy's user's session
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        reset token
        """
        try:
            user = self._db.find_user(email=email)
            if user.reset_token:
                return user.reset_token
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except (InvalidRequestError, NoResultFound):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        updates password
        """
        try:
            user = self._db.find_user(reset_token=reset_token)
            hashed = _hash_password(password)
            self._db.update_user(user.id, reset_token=None,
                                 hashed_password=hashed)
        except (InvalidRequestError, NoResultFound):
            raise ValueError

    def all(self):
        users = User.all()
        return users