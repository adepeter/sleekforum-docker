import graphene

from ...categories.models import Category

from .types import CategoryType


class CategoryQuery(graphene.ObjectType):
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()
