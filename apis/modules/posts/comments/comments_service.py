from modules.posts.comments.comments_dao import PostCommentDAO, CommentSchema
from flask import g
from dependency_injector.wiring import Provide
from bson import ObjectId
from typing import List
from modules.users.users_dao import UserDAO
import modules.users.users_service as us


class CommentService:
    user_service: us.UserService = Provide['user_service']

    def __init__(self, post_comment_schema_cls: CommentSchema.__class__) -> None:
        self.post_comment_schema_cls = post_comment_schema_cls

    def create_comment(self, payload):
        new_comment = self.post_comment_schema_cls()
        new_comment.user_id = g.user['id']
        new_comment.parent_id = payload['parent_id'] if 'parent_id' in payload  else None
        new_comment.post_id = payload['post_id']
        new_comment.content = payload['content']
        new_comment.save()

    def get_comments(self, payload):
        parent_id = payload['parent_id']
        post_id = payload['post_id']

        comments = self.post_comment_schema_cls.objects(parent_id=parent_id, post_id=post_id).order_by('-created_at')
        users: List[UserDAO] = self.user_service.get_users_by_ids(list(map(lambda x: x.user_id, comments)))

        return list(map(lambda x: self.get_comment_dto(x, users), comments))

    def get_comment_dto(self, comment: PostCommentDAO, users: List[UserDAO]):
        return {
            'content': comment.content,
            'post_id': comment.post_id,
            'user_id': comment.user_id,
            'username': list(filter(lambda x: x.id == comment.user_id, users))[0].username,
            'created_at': comment.created_at
        }
