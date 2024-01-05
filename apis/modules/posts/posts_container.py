from dependency_injector import containers, providers
from modules.posts.posts_dao import PostSchema
from modules.posts.likes.likes_dao import PostLikeSchema

import modules.posts.posts_service as posts_service
import modules.posts.likes.likes_service as likes_service


class PostContainer(containers.DeclarativeContainer):
    post_schema = providers.Factory(PostSchema)
    post_service = providers.Factory(
        posts_service.PostService, post_schema_cls=post_schema.provides)
