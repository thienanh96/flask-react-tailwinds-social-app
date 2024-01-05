from dependency_injector import containers, providers
from modules.users.users_service import UserService
from modules.users.users_dao import UserSchema


class UserContainer(containers.DeclarativeContainer):
    user_schema = providers.Factory(UserSchema)
    user_service = providers.Factory(
        UserService, user_schema_cls=user_schema.provides)
