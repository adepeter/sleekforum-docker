import graphene
from graphene_django import DjangoObjectType

from .....threads.models.thread import Thread

from ....categories.types import CategoryType


class ThreadType(DjangoObjectType):
    category = graphene.Field(CategoryType)

    class Meta:
        model = Thread
