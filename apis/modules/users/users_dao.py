from mongoengine import StringField
from common.base import BaseDAO, BaseDocument


class UserSchema(BaseDocument):
    username = StringField(required=True)
    password = StringField(required=True)
    meta = {'collection': 'users'}


class UserDAO(BaseDAO):
    username: str
    password: str
