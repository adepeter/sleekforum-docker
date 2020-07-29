from django.utils.translation import gettext_lazy as _

import graphene


class CategoryThreadInput(graphene.InputObjectType):
    """Category input that a thread belongs to"""
    id = graphene.ID(
        description=_('ID of category thread belongs to'),
        required=True
    )
    slug = graphene.String(
        description=_('slug of category thread belongs to'),
        required=True
    )


class ThreadBaseInputMixin(graphene.InputObjectType):
    """Base Input Mixin for thread manipulation
    :param category_slug, id, slug:
    """
    category_slug = graphene.String(
        description=_('slug of category thread belongs to'),
        required=True
    )
    id = graphene.ID(
        description=_('ID of the thread'),
        required=True
    )
    slug = graphene.String(
        description=_('slug of thread'),
        required=True
    )


class ThreadCreateBaseInput(graphene.InputObjectType):
    """Base input class for thread creation"""
    id = graphene.ID
    title = graphene.String(
        description=_('title of new thread'),
    )
    slug = graphene.String(
        description=_('slug of new thread. if not provided, title will be used'),
    )
    tags = graphene.List(
        graphene.String,
        description=_('tags to associate thread')
    )
    content = graphene.String(
        description=_('content of thread'),
    )


class ThreadCreateInput(graphene.InputObjectType):
    """Input for new thread creation"""
    category = graphene.InputField(
        CategoryThreadInput,
        description=_('category thread should to'),
        required=True
    )
    thread = graphene.InputField(
        ThreadCreateBaseInput,
        description=_('new thread properties'),
        required=True
    )


class ThreadEditPatchInputMixin(ThreadCreateInput):
    """Just a subclass to rename parent input class"""


class ThreadEditInput(graphene.InputObjectType):
    """Input for thread modification"""
    thread = graphene.InputField(
        ThreadBaseInputMixin,
        description=_('property of thread to be edited'),
        required=True
    )
    patch = graphene.InputField(
        ThreadEditPatchInputMixin,
        description=_('new properties for thread'),
    )


class ThreadDeleteInput(ThreadBaseInputMixin):
    """Input for thread deletion"""
