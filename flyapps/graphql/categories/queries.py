import graphene

from ...categories.models import Category

from .types import CategoryType


class CategoryQuery(graphene.ObjectType):
    categories = graphene.List(
        CategoryType,
        base=graphene.Boolean(default_value=True)
    )

    def resolve_categories(self, info, **kwargs):
        """List all categories"""
        if kwargs.get('base') is True:
            return Category.objects.filter(parent__isnull=True)
        return Category.objects.all()
