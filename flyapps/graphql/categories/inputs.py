import graphene
from .types import CategoryType


class CategoryInput(graphene.InputObjectType):
    id = graphene.Int()
    name = graphene.String(required=True, description='Category description')
    slug = graphene.String(description='Short name to access category')
    description = graphene.String()