from dependency_injector import containers, providers
from modules.posts.likes.likes_dao import PostLikeSchema
import modules.posts.likes.likes_service as likes_service


class PostLikeContainer(containers.DeclarativeContainer):
    post_like_schema = providers.Factory(PostLikeSchema)
    post_like_service = providers.Factory(
        likes_service.LikeService, post_like_schema_cls=post_like_schema.provides)
