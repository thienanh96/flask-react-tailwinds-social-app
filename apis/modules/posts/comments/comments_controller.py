from flask_restx import Resource, fields, Namespace
from dependency_injector.wiring import Provide
from modules.posts.comments.comments_service import CommentService
from common.decorators import login_required
from flask import request

ns = Namespace('post_comments')

post_comment_request_model = ns.model('CreatePostCommentRequestModel', {
    'parent_id': fields.String(required=False, description='The parent id of comment'),
    'content': fields.String(required=True, description='The content of comment'),
})

post_comment_model = ns.model('PostCommentModel', {
    'id': fields.String(required=False, description='The id of comment'),
    'parentId': fields.String(required=False, description='The parent id of comment', attribute='parent_id'),
    'username': fields.String(required=True, description='The name of comment user'),
    'postId': fields.String(required=True, description='The name of comment user', attribute='post_id'),
    'content': fields.String(required=True, description='The content of comment'),
    'createdAt': fields.DateTime(required=True, description='The creation datetime of comment', attribute='created_at'),
})

post_comments_model = ns.model('PostCommentsModel', {
    'comments': fields.List(fields.Nested(post_comment_model)),
    'paths': fields.List(fields.String)
})


get_post_comments_request_model = ns.model('GetPostCommentsRequestModel', {
    'post_id': fields.String(required=True, description='The id of post'),
    'parent_id': fields.String(required=False, description='The parent id of comment'),
})


@ns.route('')
class PostLikeRoute(Resource):
    post_comment_service: CommentService = Provide['post_comment_service']

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    '''Create comment'''
    @ns.doc('create_post_comment')
    @ns.expect(post_comment_request_model, validate=True)
    @ns.marshal_with(post_comment_model)
    @login_required
    def post(self):
        return self.post_comment_service.create_comment(request.view_args['id'], ns.payload)

    '''Get comments'''
    @ns.doc('get_post_comments')
    @ns.marshal_with(post_comments_model)
    @login_required
    def get(self):
        return self.post_comment_service.get_comments(
            request.view_args['id'], request.args.get('parentId'))
