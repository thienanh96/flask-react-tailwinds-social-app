from modules.users.users_dao import UserDAO, UserSchema
from werkzeug.exceptions import BadRequest, Unauthorized
import jwt
import bcrypt
from typing import List
from bson import ObjectId


class UserService:
    def __init__(self, user_schema_cls: UserSchema.__class__) -> None:
        self.user_schema_cls = user_schema_cls

    def register(self, payload):
        new_user = self.user_schema_cls()
        new_user.username = payload['username']

        existing_user: UserDAO or None = self.user_schema_cls.objects(
            username=payload['username']).first()

        if existing_user is not None:
            raise BadRequest('User exists')

        salt = bcrypt.gensalt()
        new_user.password = bcrypt.hashpw(
            payload['password'].encode('utf-8'), salt).decode('utf-8')
        new_user.save()

        user: UserDAO = self.user_schema_cls.objects(
            username=new_user.username).first()

        return {
            'id': user.id,
            'username': user.username,
            'token': self.get_user_token(user=user)
        }

    def get_user_token(self, user: UserDAO):
        return jwt.encode(
            {"username": user.username, "id": str(user.id)}, "secret", algorithm="HS256")

    def login(self, payload):
        username = payload['username']
        password = payload['password']
        existing_user: UserDAO or None = self.user_schema_cls.objects(
            username=username).first()
        if existing_user is None:
            raise BadRequest('User not found')

        password_matched = bcrypt.checkpw(
            password.encode('utf-8'), existing_user.password.encode('utf-8'))

        if password_matched is False:
            raise BadRequest('Invalid password')

        return {
            'id': existing_user.id,
            'username': existing_user.username,
            'token': self.get_user_token(user=existing_user)
        }

    def get_logged_in_user_info(self, token: str or None):
        if token is None:
            raise Unauthorized('Token does not exist')
        return jwt.decode(token, 'secret', ["HS256"])

    def get_users_by_ids(self, user_ids: List[ObjectId]) -> List[UserDAO]:
        return self.user_schema_cls.objects(id__in=user_ids)
