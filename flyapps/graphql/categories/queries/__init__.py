import graphene
from django.shortcuts import get_object_or_404

from ....categories.models import Category

from ..types import CategoryType


class CategoryQueries:
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()


class SubcategoryQueries:
    category = graphene.Field(CategoryType, slug=graphene.String())
    subcategories = graphene.List(CategoryType)

    def resolve_category(self, info, **kwargs):
        return get_object_or_404(Category, slug__iexact=kwargs.get('slug'))

    def resolve_subcategories(self, info, **kwargs):
        return Category.objects.filter(parent=self.category)
