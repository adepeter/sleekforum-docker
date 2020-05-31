import graphene

from ...categories.models import Category

from .inputs import CategoryInput
from .types import CategoryType


class CategoryPayload(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        category = Category.objects.create(name=name)
        return CategoryPayload(category=category)


class CategoryInputPayload(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        input = CategoryInput(required=True)

    def mutate(self, info, input=None):
        category = Category.objects.create(name=input.name)
        return CategoryInputPayload(category=category)


class CategoryDeletePayload(graphene.Mutation):
    categories = graphene.List(CategoryType)
    
    class Arguments:
        id = graphene.Int(required=True)
        
    def mutate(self, info, id, **kwargs):
        try:
            category = Category.objects.get(id=id).delete()
        except Category.DoesNotExist:
            raise ValueError('Category does not exist')
        return CategoryDeletePayload(categories=Category.objects.all())
    
class CreateAndListPayload(graphene.Mutation):
    category = graphene.Field(CategoryType)
    categories = graphene.List(CategoryType)

    class Arguments:
        slug = graphene.String()
        name = graphene.String(required=True)

    def mutate(root, info, name, slug=None) -> str:
        parent = None
        if slug is not None:
            parent = Category.objects.get(slug__iexact=parent)
        category = Category.objects.create(name=name, parent=parent)
        return CreateAndListPayload(category=category)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()