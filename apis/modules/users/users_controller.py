from flask_restx import Resource, fields, Namespace
from flask_restx._http import HTTPStatus
from modules.users.users_service import UserService
from common.decorators import login_required
from flask import g
from dependency_injector.wiring import Provide


ns = Namespace('users')

user_model = ns.model('UserModel', {
    'id': fields.String(required=True, description=''),
    'username': fields.String(required=True, description='The username of an user'),
    'token': fields.String(required=False, description='User token'),
})

login_register_user_request_model = ns.model('LoginUserModel', {
    'username': fields.String(required=True, description='The username of an user'),
    'password': fields.String(required=True, description='The password of an user'),
})


@ns.route('/register')
class RegisterUserRoute(Resource):
    user_service: UserService = Provide['user_service']

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    '''Register new user'''
    @ns.doc('register_user')
    @ns.expect(login_register_user_request_model, validate=True)
    @ns.marshal_list_with(user_model)
    def post(self):
        return self.user_service.register(ns.payload)


@ns.route('/login')
class LoginUserRoute(Resource):
    user_service: UserService = Provide['user_service']

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    '''Login user'''
    @ns.doc('login_user')
    @ns.expect(login_register_user_request_model, validate=True)
    @ns.marshal_with(user_model, code=HTTPStatus.ACCEPTED)
    def post(self):
        return self.user_service.login(ns.payload)


@ns.route('/current')
class CurrentUserRoute(Resource):
    user_service: UserService = Provide['user_service']

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    '''Get current user'''
    @ns.doc('current_user')
    @ns.marshal_with(user_model, code=HTTPStatus.ACCEPTED)
    @login_required
    def get(self, *args):
        return g.user
