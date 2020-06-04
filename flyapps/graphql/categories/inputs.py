import graphene


class BaseCategoryInputMixin(graphene.InputObjectType):
    """Base input class for mutation"""
    id = graphene.ID()
    slug = graphene.String()


class CategoryCreateInput(BaseCategoryInputMixin):
    """Input for a category create"""
    id = graphene.ID
    name = graphene.String()
    slug = graphene.String()
    description = graphene.String()
    parent = graphene.Field(lambda: CategoryCreateInput)


class CategoryPatchInput(CategoryCreateInput):
    """A mediator patch input that calls parent category"""
    parent = BaseCategoryInputMixin()


class CategoryEditInput(BaseCategoryInputMixin):
    """Input for category edit"""
    patch = CategoryPatchInput()


class CategoryDeleteInput(BaseCategoryInputMixin):
    """Input for a category delete"""
