from graphene_django.types import DjangoObjectType

from .....threads.models.post import Post


class PostType(DjangoObjectType):
    class Meta:
        model = Post
