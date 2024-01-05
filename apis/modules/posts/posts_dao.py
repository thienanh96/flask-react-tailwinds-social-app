from mongoengine import StringField, ObjectIdField, IntField
from common.base import BaseDAO, BaseDocument
from bson import ObjectId


class PostSchema(BaseDocument):
    title = StringField(required=True)
    content = StringField(required=True)
    created_by = ObjectIdField(required=True)
    like_count = IntField(default=0)
    dislike_count = IntField(default=0)
    meta = {'collection': 'posts'}


class PostDAO(BaseDAO):
    title: str
    content: str
    created_by: ObjectId
    like_count: int
    dislike_count: int
