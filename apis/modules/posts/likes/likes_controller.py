import modules.posts.likes.likes_container as likes_container

from flask_restx import Resource, fields, Namespace
from dependency_injector.wiring import Provide
from modules.posts.likes.likes_dao import PostLikeType
from modules.posts.likes.likes_service import LikeService
from common.decorators import login_required


ns = Namespace('post_likes')

post_like_request_model = ns.model('CreatePostLikeRequestModel', {
    'post_id': fields.String(required=True, description='The id of post'),
    'type': fields.Integer(required=True, description='The type of like', enum=[PostLikeType.LIKE, PostLikeType.DISLIKE]),
})


@ns.route('')
class PostLikeRoute(Resource):
    post_like_service: LikeService = Provide['post_like_service']

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)

    '''Create like'''
    @ns.doc('create_post_like')
    @ns.expect(post_like_request_model, validate=True)
    @login_required
    def post(self):
        print('--ss--')
        return self.post_like_service.create_like(ns.payload)

    '''delete like'''
    @ns.doc('create_post_like')
    @ns.expect(post_like_request_model, validate=True)
    @login_required
    def delete(self):
        return self.post_like_service.delete_like(ns.payload)
