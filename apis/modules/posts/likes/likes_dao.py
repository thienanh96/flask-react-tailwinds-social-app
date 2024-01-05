from mongoengine import StringField, ObjectIdField, EnumField
from common.base import BaseDAO, BaseDocument
from bson import ObjectId
from enum import Enum


class PostLikeType(Enum):
    LIKE = 1
    DISLIKE = 2


class PostLikeSchema(BaseDocument):
    post_id = ObjectIdField(required=True)
    user_id = ObjectIdField(required=True)
    type = EnumField(PostLikeType, required=True)
    meta = {'collection': 'post_likes'}


class PostLikeDAO(BaseDAO):
    post_id: ObjectId
    user_id: ObjectId
    type: PostLikeType
