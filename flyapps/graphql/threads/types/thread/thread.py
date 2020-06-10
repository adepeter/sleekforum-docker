import graphene
from graphene_django.types import DjangoObjectType

from .....threads.models.thread import Thread

from ....categories.types import CategoryType
from ....users.types.user import UserType


class ThreadType(DjangoObjectType):
    category = graphene.Field(graphene.NonNull(CategoryType))
    starter = graphene.Field(graphene.NonNull(UserType))

    class Meta:
        model = Thread
