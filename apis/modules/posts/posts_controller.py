from flask_restx import Resource, fields, Namespace
from dependency_injector.wiring import Provide
from common.decorators import login_required


ns = Namespace('posts')

post_model = ns.model('PostModel', {
    'id': fields.String(required=True, description=''),
    'title': fields.String(required=True, description='The title of post'),
    'content': fields.String(required=True, description='The content of post'),
    'authorName': fields.String(required=True, description='The name of author', attribute='author_name'),
    'likeCount': fields.Integer(require=True, description='Like count of post', attribute='like_count'),
    'dislikeCount': fields.Integer(require=True, description='Dislike count of post', attribute='dislike_count'),
    'createdAt': fields.DateTime(required=True, description='The creation datetime of post', attribute='created_at'),
    'likedByMe': fields.Boolean(required=True, attribute='liked_by_me'),
    'dislikedByMe': fields.Boolean(required=True, attribute='disliked_by_me'),
})


create_post_request_model = ns.model('CreatePostRequestModel', {
    'title': fields.String(required=True, description='The title of post'),
    'content': fields.String(required=True, description='The content of post'),
    'created_by': fields.String(required=True, description='The author of post'),
})


@ns.route('')
class PostRoute(Resource):
    post_service = Provide['post_service']

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    '''Create post'''
    @ns.doc('create_post')
    @ns.expect(create_post_request_model, validate=True)
    @ns.marshal_with(post_model)
    @login_required
    def post(self):
        return self.post_service.create_post(ns.payload)

    '''Get posts'''
    @ns.doc('get_posts')
    @ns.marshal_list_with(post_model)
    @login_required
    def get(self):
        return self.post_service.get_posts()
