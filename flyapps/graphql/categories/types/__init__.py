import graphene

from graphene_django.types import DjangoObjectType

from ....categories.models import Category


class CategoryType(DjangoObjectType):
    parent = graphene.Field(lambda: CategoryType)

    class Meta:
        model = Category
        fields = '__all__'
