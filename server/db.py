from sqlalchemy import create_engine, select
from sqlalchemy.orm  import sessionmaker
from user import User, Base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB():
    def __init__(self):
        self.engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_user(self, email, hashed_password):
        user = User(email=email, hashed_password=hashed_password)
        self.session.add(user)
        self.session.commit()
        return user

    def find_user(self, **kwargs):
        if not kwargs:
            raise InvalidRequestError
        column_names = User.__table__.columns.keys()
        filters = []
        for key, value in kwargs.items():
            if key not in column_names:
                raise InvalidRequestError
            column = getattr(User, key)
            filters.append(column == value)
        if not filters:
            raise NoResultFound
        stment = select(User).where(*filters)
        result = self.session.execute(stment)
        user = result.scalars().first()
        return user

    def update_user(self, email, **kwargs):
        user = self.find_user(email=email)
        for key, value in kwargs.items():
            if key not in User.__table__.columns.keys():
                raise ValueError
            setattr(user, key, value)
            self.session.commit()

    def all(self):
        users = self.session.scalars(select(User)).all()
        return users
