from modules.posts.comments.comments_dao import PostCommentDAO, CommentSchema
from flask import g
from dependency_injector.wiring import Provide
from bson import ObjectId, objectid
from typing import List
from modules.users.users_dao import UserDAO
import modules.users.users_service as us


class CommentService:
    user_service: us.UserService = Provide['user_service']

    def __init__(self, post_comment_schema_cls: CommentSchema.__class__) -> None:
        self.post_comment_schema_cls = post_comment_schema_cls

    def create_comment(self, post_id, payload):
        new_comment = self.post_comment_schema_cls()
        new_comment.user_id = g.user['id']
        new_comment.parent_id = payload['parent_id'] if 'parent_id' in payload else None
        new_comment.post_id = post_id
        new_comment.content = payload['content']
        new_comment.save()

    def get_comments(self, post_id, parent_id):
        print('--dd', parent_id)
        parent_id_obj = None if parent_id is None else objectid.ObjectId(
            parent_id)

        comments = self.post_comment_schema_cls.objects(
            parent_id=parent_id_obj, post_id=post_id).order_by('-created_at')

        users: List[UserDAO] = self.user_service.get_users_by_ids(
            list(map(lambda x: x.user_id, comments)))

        paths = []

        self.get_comment_path(
            comment_id=parent_id_obj, paths=paths)

        return {
            'comments': list(map(lambda x: self.get_comment_dto(x, users), comments)),
            'paths': paths
        }

    def get_comment_dto(self, comment: PostCommentDAO, users: List[UserDAO]):
        return {
            'id': comment.id,
            'content': comment.content,
            'post_id': str(comment.post_id),
            'parent_id': str(comment.parent_id) if comment.parent_id is not None else None,
            'user_id': str(comment.user_id),
            'username': list(filter(lambda x: x.id == comment.user_id, users))[0].username,
            'created_at': comment.created_at.isoformat()
        }

    def get_comment_path(self, comment_id: ObjectId | None, paths: List[str]):
        if (comment_id is None):
            return paths

        comment = self.post_comment_schema_cls.objects(id=comment_id).first()

        if comment is not None:
            paths.append(str(comment.id))
            self.get_comment_path(comment.parent_id, paths=paths)
        else:
            return paths
