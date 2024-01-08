from flask_restx import Resource, fields, Namespace
from dependency_injector.wiring import Provide
from modules.posts.comments.comments_service import CommentService
from common.decorators import login_required


ns = Namespace('post_comments')

post_comment_request_model = ns.model('CreatePostCommentRequestModel', {
    'parent_id': fields.String(required=False, description='The parent id of comment'),
    'post_id': fields.String(required=True, description='The id of post'),
    'content': fields.String(required=True, description='The content of comment'),
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
    @login_required
    def post(self):
        return self.post_comment_service.create_comment(ns.payload)

    '''Get comments'''
    @ns.doc('get_post_comments')
    @login_required
    def get(self):
        return self.post_comment_service.get_comments(ns.payload)
