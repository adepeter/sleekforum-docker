import graphene

from ....categories.models import Category

from ..types import CategoryType


class CreateCategory(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String(required=True)
    description = graphene.String()
    parent = graphene.Field(CategoryType)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name, parent=None, **kwargs):
        category = Category.objects.create(name=name)
        if kwargs.get('parent') is not None:
            category.parent = category
            category.save(update_fields=['parent'])
        return CreateCategory(
            id=category.id,
            name=category.name,
            slug=category.slug,
            parent=category.parent,
        )

class CategoryMutations(graphene.ObjectType):
    create_category = CreateCategory.Field()