from flask_restx import fields, Namespace, Model
from flask import current_app
from werkzeug.exceptions import InternalServerError
from flask_pymongo.wrappers import Database
from flask_pymongo import PyMongo


def get_paginated_data(api: Namespace, entity: Namespace, prefix: str | None) -> Model:
    return api.model('Paginated{}'.format(prefix), {
        'data': fields.List(fields.Nested(entity)),
        'page': fields.Integer(),
        'per_page': fields.Integer()
    })


def get_request_filters_with_pagination(api: Namespace, prefix: str, model: Model):
    return api.model('{}WithPagination'.format(prefix), {
        'filters': fields.Nested(allow_null=True, model=model),
        'skip': fields.Integer(default=0),
        'limit': fields.Integer(default=10)
    })


def get_db() -> Database:
    db = PyMongo(current_app).db
    if db is None:
        raise InternalServerError('Database is not initialized')

    return db
