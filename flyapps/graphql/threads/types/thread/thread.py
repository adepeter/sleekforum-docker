import graphene
from graphene_django.types import DjangoObjectType

from .....threads.models.thread import Thread

from ....categories.types import CategoryType
from ....users.types.user import UserType

from ..post.post import PostType


class ThreadType(DjangoObjectType):
    category = graphene.Field(graphene.NonNull(CategoryType))
    starter = graphene.Field(graphene.NonNull(UserType))
    posts = graphene.List(PostType)

    class Meta:
        model = Thread

    def resolve_posts(self, info, **kwargs):
        return self.posts.all()
