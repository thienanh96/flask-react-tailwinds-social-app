import os
import configparser

from flask import Flask
from flask_restx import Api
from mongoengine import connect
from werkzeug.middleware.proxy_fix import ProxyFix
from modules.users.users_controller import ns as userNs
from modules.posts.posts_controller import ns as postNs
from modules.posts.likes.likes_controller import ns as postLikeNs
from flask_cors import CORS
from modules.users.users_container import UserContainer
from modules.posts.posts_container import PostContainer
from modules.posts.likes.likes_container import PostLikeContainer


def connect_db(app: Flask):
    connect(host=app.config['MONGO_URI'])


def parse_config(app: Flask):
    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join(".config")))
    app.config['MONGO_URI'] = config['PROD']['DB_URI']


def add_namespaces(api: Api):
    api.add_namespace(userNs, '/users')
    api.add_namespace(postLikeNs, '/posts/likes')
    api.add_namespace(postNs, '/posts')


def wire_modules():
    UserContainer().wire(modules=[
        "modules.posts.posts_service", "modules.users.users_controller", "common.decorators", "modules.posts.posts_controller", "modules.posts.likes.likes_controller"])
    PostContainer().wire(
        modules=['modules.posts.posts_controller', 'modules.posts.likes.likes_service'])
    PostLikeContainer().wire(
        modules=['modules.posts.likes.likes_controller', 'modules.posts.posts_service'])


if __name__ == '__main__':
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    cors = CORS(app, origins=['http://localhost:5173'])
    parse_config(app=app)

    with app.app_context():
        api = Api(app, version='1.0', title='Flask App',
                  description='A simple Flask App')

        connect_db(app=app)
        add_namespaces(api=api)
        wire_modules()

        app.run(debug=True)
