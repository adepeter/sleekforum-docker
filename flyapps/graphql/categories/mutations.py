import graphene

from .payloads import (
    CategoryPayload,
    CategoryInputPayload,
    CategoryDeletePayload,
    CreateAndListPayload,
)


class CategoryMutations(graphene.ObjectType):
    create_category = CategoryPayload.Field()
    category_with_input = CategoryInputPayload.Field()
    category_delete = CategoryDeletePayload.Field()
    create_and_list = CreateAndListPayload.Field()
