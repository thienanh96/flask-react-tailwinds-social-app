from mongoengine import ObjectIdField, StringField
from common.base import BaseDAO, BaseDocument
from bson import ObjectId


class CommentSchema(BaseDocument):
    post_id = ObjectIdField(required=True)
    user_id = ObjectIdField(required=True)
    parent_id = ObjectIdField(required=False)
    content = StringField(required=True)

    meta = {'collection': 'post_comments'}


class PostCommentDAO(BaseDAO):
    post_id: ObjectId
    user_id: ObjectId
    parent_id: ObjectId
    content: str
