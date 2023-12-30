from modules.users.users_dao import UserDAO, UserSchema
from werkzeug.exceptions import BadRequest, Unauthorized
from typing import List
import jwt
import bcrypt


class UserService:
    def register(self, payload):
        new_user = UserSchema()
        new_user.username = payload['username']

        existing_user: UserDAO | None = UserSchema.objects(
            username=payload['username']).first()

        if existing_user is None:
            raise BadRequest('User exists')

        salt = bcrypt.gensalt()
        new_user.password = bcrypt.hashpw(
            payload['password'].encode('utf-8'), salt).decode('utf-8')
        new_user.save()

        user: UserDAO = UserSchema.objects(username=new_user.username).first()

        return {
            'id': user.id,
            'username': user.username,
            'token': self.get_user_token(user=user)
        }

    def get_user_token(self, user: UserDAO):
        print(user.id, str(user.id))
        return jwt.encode(
            {"username": user.username, "id": str(user.id)}, "secret", algorithm="HS256")

    def login(self, payload):
        username = payload['username']
        password = payload['password']
        existing_user: UserDAO | None = UserSchema.objects(
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

    def get_logged_in_user_info(self, token: str | None):
        if token is None:
            raise Unauthorized('Token does not exist')
        return jwt.decode(token, 'secret', ["HS256"])
