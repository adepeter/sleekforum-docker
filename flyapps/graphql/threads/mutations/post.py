import graphene

from ..payloads.post import (
    PostCreatePayload,
    PostEditPayload
)


class PostMutation(graphene.ObjectType):
    post_create = PostCreatePayload.Field()
    post_edit = PostEditPayload.Field()
