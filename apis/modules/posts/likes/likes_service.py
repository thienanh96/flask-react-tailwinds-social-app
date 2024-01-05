from modules.posts.likes.likes_dao import PostLikeSchema, PostLikeType, PostLikeDAO
from flask import g
from dependency_injector.wiring import Provide
from bson import ObjectId
from typing import List


class LikeService:
    post_service = Provide['post_service']

    def __init__(self, post_like_schema_cls: PostLikeSchema.__class__) -> None:
        self.post_like_schema_cls = post_like_schema_cls

    def create_like(self, payload):
        new_like = self.post_like_schema_cls()
        new_like.user_id = g.user['id']
        new_like.type = payload['type']
        new_like.post_id = payload['post_id']

        existing_like = self.post_like_schema_cls.objects(
            user_id=new_like.user_id, post_id=new_like.post_id, type=new_like.type).first()

        if existing_like is not None:
            return None

        new_like.save()

        self.delete_like(
            {'post_id': payload['post_id'], 'type': PostLikeType.DISLIKE if payload['type'] == PostLikeType.LIKE.value else PostLikeType.LIKE})
        self.update_post_like_count(
            post_id=payload['post_id'], type=payload['type'])

    def delete_like(self, payload):
        existing_like = self.post_like_schema_cls.objects(
            user_id=g.user['id'], post_id=payload['post_id'], type=payload['type']).first()

        if existing_like is not None:
            existing_like.delete()
            self.update_post_like_count(
                post_id=payload['post_id'], type=payload['type'])

    def update_post_like_count(self, post_id: ObjectId, type: PostLikeType):
        if type == PostLikeType.LIKE.value:
            like_count = self.post_like_schema_cls.objects(
                post_id=post_id, type=PostLikeType.LIKE).count()
            self.post_service.update_post_likes(
                post_id=post_id, like_count=like_count, dislike_count=None)
        elif type == PostLikeType.DISLIKE.value:
            dislike_count = self.post_like_schema_cls.objects(
                post_id=post_id, type=PostLikeType.DISLIKE).count()
            self.post_service.update_post_likes(
                post_id=post_id, like_count=None, dislike_count=dislike_count)

    def is_like_or_dislike_by_me(self, post_ids: List[ObjectId]):
        post_likes: List[PostLikeDAO] = self.post_like_schema_cls.objects(
            post_id__in=post_ids, user_id=g.user['id'])

        like_res = []
        for post_id in post_ids:
            is_liked_by_me = len(list(filter(lambda x: x.type == PostLikeType.LIKE and str(
                post_id) == str(x.post_id), post_likes))) != 0
            is_disliked_by_me = len(list(filter(lambda x: x.type == PostLikeType.DISLIKE and str(
                post_id) == str(x.post_id), post_likes))) != 0
            res = {
                'is_liked_by_me': is_liked_by_me and is_disliked_by_me == False,
                'is_disliked_by_me': is_disliked_by_me and is_liked_by_me == False
            }
            like_res.append(res)

        return like_res
