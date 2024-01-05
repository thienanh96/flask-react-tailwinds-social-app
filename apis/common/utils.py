from flask_restx import fields, Namespace, Model


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
