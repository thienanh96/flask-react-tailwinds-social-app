from functools import wraps
from flask import g, request, redirect, url_for
from flask import request
from werkzeug.exceptions import Unauthorized
from modules.users.users_service import UserService


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            user_service = UserService()
            g.user = user_service.get_logged_in_user_info(
                request.headers.get('Token'))
        except Exception as e:
            raise Unauthorized()

        return f(*args, **kwargs)
    return decorated_function
