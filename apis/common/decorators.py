from functools import wraps
from flask import g, request
from werkzeug.exceptions import Unauthorized
from modules.users.users_service import UserService
from dependency_injector.wiring import inject, Provide
from modules.users.users_container import UserContainer


def login_required(f):
    @wraps(f)
    @inject
    def decorated_function(*args, user_service: UserService = Provide[UserContainer.user_service]):
        try:
            g.user = user_service.get_logged_in_user_info(
                request.headers.get('Token'))
            print(g.user)
        except Exception as e:
            print(e)
            raise Unauthorized()

        return f(*args)
    return decorated_function
