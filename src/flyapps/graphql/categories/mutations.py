import graphene

from .payloads import (
    CategoryCreatePayload,
    CategoryDeletePayload,
    CategoryEditPayload
)


class CategoryMutation(graphene.ObjectType):
    category_create = CategoryCreatePayload.Field()
    category_delete = CategoryDeletePayload.Field()
    category_edit = CategoryEditPayload.Field()
