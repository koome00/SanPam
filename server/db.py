import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm  import sessionmaker
from user import User, Base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB():
    def __init__(self):
        self.engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.session = None

    def _session(self):
        if self.session is None:
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        return self.session

    def add(self, email, hashed_password):
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user(self, **kwargs):
        if kwargs is None:
            raise InvalidRequestError
        column_names = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in column_names:
                raise InvalidRequestError
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id, **kwargs):
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in user.__table__.columns.keys():
                raise ValueError
            setattr(user, key, value)
            self._session.commit()
