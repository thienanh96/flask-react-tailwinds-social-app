from dependency_injector import containers, providers
from modules.posts.comments.comments_dao import CommentSchema
import modules.posts.comments.comments_service as comment_service


class PostCommentContainer(containers.DeclarativeContainer):
    post_comment_schema = providers.Factory(CommentSchema)
    post_comment_service = providers.Factory(
        comment_service.CommentService, post_comment_schema_cls=post_comment_schema.provides)
