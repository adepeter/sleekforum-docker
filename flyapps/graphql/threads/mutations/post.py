import graphene

from ..payloads.post import (
    PostCreatePayload,
    PostEditPayload,
    PostDeletePayload
)


class PostMutation(graphene.ObjectType):
    post_create = PostCreatePayload.Field()
    post_edit = PostEditPayload.Field()
    post_delete = PostDeletePayload.Field()
