import graphene


class CategoryThreadInput(graphene.InputObjectType):
    id = graphene.ID()
    slug = graphene.String()


class ThreadBaseInputMixin(graphene.InputObjectType):
    id = graphene.ID()
    slug = graphene.String()


class ThreadCreateBaseInput(graphene.InputObjectType):
    id = graphene.ID
    title = graphene.String()
    slug = graphene.String()
    tags = graphene.List(graphene.String)
    content = graphene.String()


class ThreadCreateInput(graphene.InputObjectType):
    category = graphene.InputField(CategoryThreadInput)
    thread = graphene.InputField(ThreadCreateBaseInput)


class ThreadEditPatchInputMixin(ThreadCreateInput):
    """Just a subclass to rename parent input class"""


class ThreadEditInput(graphene.InputObjectType):
    thread = graphene.InputField(ThreadBaseInputMixin)
    patch = graphene.InputField(ThreadEditPatchInputMixin)


class ThreadDeleteInput(ThreadBaseInputMixin):
    category = graphene.String()
