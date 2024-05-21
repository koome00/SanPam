from db import DB
from user import User
database = DB()
user = User(email="koomemc@gmail.com", hashed_password="348234834")
# user = database.add_user(email="ko00omemc@gmail.com", hashed_password="348234834")
print(user.to_dict())