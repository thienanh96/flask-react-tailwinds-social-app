from modules.posts.posts_dao import PostDAO, PostSchema
from bson import objectid, ObjectId
from modules.users.users_dao import UserDAO
from dependency_injector.wiring import Provide
from typing import List, Dict
import modules.posts.likes.likes_service as ls
import modules.users.users_service as us


class PostService:
    user_service: us.UserService = Provide['user_service']
    post_like_service: ls.LikeService = Provide['post_like_service']
    post_comments_service = Provide['post_comment_service']

    def __init__(self, post_schema_cls: PostSchema.__class__) -> None:
        self.post_schema_cls = post_schema_cls

    def create_post(self, payload):
        new_post = self.post_schema_cls()
        new_post.created_by = objectid.ObjectId(payload['created_by'])
        new_post.content = payload['content']
        new_post.title = payload['title']
        new_post.save()

        post_dao: PostDAO = self.post_schema_cls.objects(
            id=new_post.id).first()
        
        return self.get_posts_dto(posts_dao=[post_dao])[0]

    def get_posts(self) -> List[PostDAO]:
        db_posts: List[PostDAO] = self.post_schema_cls.objects().order_by(
            '-created_at')
        
        return self.get_posts_dto(posts_dao=db_posts)

    def get_posts_dto(self, posts_dao: List[PostDAO]):
        author_ids = list(map(lambda x: x.created_by, posts_dao))
        users: List[UserDAO] = self.user_service.get_users_by_ids(author_ids)

        is_like_or_dislike_by_me = self.post_like_service.is_like_or_dislike_by_me(
            list(map(lambda x: x.id, posts_dao)))

        posts = []
        for idx, db_post in enumerate(posts_dao):
            post = {}
            post['id'] = db_post.id
            post['content'] = db_post.content
            post['title'] = db_post.title
            post['like_count'] = db_post.like_count
            post['dislike_count'] = db_post.dislike_count
            post['author_name'] = list(
                filter(lambda x: x.id == db_post.created_by, users))[0].username
            post['created_at'] = db_post.created_at
            post['liked_by_me'] = is_like_or_dislike_by_me[idx]['is_liked_by_me']
            post['disliked_by_me'] = is_like_or_dislike_by_me[idx]['is_disliked_by_me']
            post['comments'] = [] # not loaded with list posts
            posts.append(post)

        return posts

    def get_post_by_id(self, post_id: ObjectId) -> PostDAO:
        return self.post_schema_cls.objects(id=post_id).first()

    def update_post_likes(self, post_id: ObjectId, like_count: int or None, dislike_count: int or None):
        posts = self.post_schema_cls.objects(id=post_id)
        if len(posts) > 0:
            if like_count is not None:
                posts.update_one(like_count=like_count)
            elif dislike_count is not None:
                posts.update_one(dislike_count=dislike_count)
