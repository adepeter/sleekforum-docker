import graphene
from django.shortcuts import get_object_or_404

from ...categories.models import Category

from .types import CategoryType


class RootCategoryQuery:
    category = graphene.Field(CategoryType, slug=graphene.String())
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_category(self, info, slug):
        return get_object_or_404(Category, slug__iexact=slug)
