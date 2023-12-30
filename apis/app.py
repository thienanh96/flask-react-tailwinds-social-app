import os
import configparser

from flask import Flask
from flask_restx import Api
from mongoengine import connect
from werkzeug.middleware.proxy_fix import ProxyFix
from modules.users.users_controller import ns as userNs
from flask_cors import cross_origin, CORS


def connect_db(app: Flask):
    connect(host=app.config['MONGO_URI'])


def parse_config(app: Flask):
    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join(".config")))
    app.config['MONGO_URI'] = config['PROD']['DB_URI']


def add_namespaces(api: Api):
    api.add_namespace(userNs, '/users')


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

        app.run(debug=True)
