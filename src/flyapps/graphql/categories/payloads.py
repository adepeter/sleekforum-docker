from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

import graphene
from graphql import GraphQLError

from ...categories.models import Category

from .inputs import (
    BaseCategoryInputMixin,
    CategoryCreateInput,
    CategoryDeleteInput,
    CategoryEditInput,
    CategoryPatchInput,
)
from .types import CategoryType


def dictify(param):
    """Returns a key: value dictionary"""
    return {field: value for field, value in param.items()}


def dictify_inputs(input_obj, input_type):
    """Return a dictionary key: value par for an InputTypeObject parameter"""
    if isinstance(input_obj, input_type):
        return dictify(input_obj)
    return None


class CategoryCreatePayload(graphene.Mutation):
    """
    This Payload is for creating new category.
    It is a complex multi-functional category creator.
    It accepts just one parameter 'input',
    This input can in turn accept 1 - 4 parameters namely:
    1. name (Name for category been created - constant)
    2. slug (querable url for category been created - optional) if
    not supplied, 'name' above will be used
    3. description (description of category been created - optional)
    4. parent (if supplied, new category created will be attached to this parent - optional):
        a. Lookup: Parent accepts 2 parameters for lookup (ie id and slug of parent).
        If it exists, the new category gets attached to it.
        b. Create: Parent accepts 1 - 2 (ie name: constant, description: optional) parameters
        other than the used for look up and creates a new base category as parent.
        Then attach the category created in 1 to it.
    """
    category = graphene.Field(CategoryType)
    is_created = graphene.Boolean()

    class Arguments:
        input = CategoryCreateInput(required=True)

    def mutate(self, info, input):
        user = info.context.user
        if not user.is_authenticated and not (user.is_staff or user.is_superuser):
            raise PermissionDenied('You do not have the permission to perform this operation')
        parent = None
        if hasattr(input, 'parent'):
            items = getattr(input, 'parent', None)
            if items is not None:
                dump = {field: value for field, value in items.items()}
                if ('id' or 'pk') and 'slug' in dump:
                    parent = get_object_or_404(
                        Category, id=dump['id'] or dump['pk'],
                        slug__iexact=dump['slug']
                    )
                else:
                    parent, create = Category.objects.get_or_create(**dump)
        category = Category.objects.create(name=input.name, parent=parent)
        is_created = True
        return CategoryCreatePayload(category=category, is_created=is_created)


class CategoryEditPayload(graphene.Mutation):
    """
    This is a payload for editing a category.
    Very similar in function to categoryCreate counter part
    """
    category = graphene.Field(CategoryType)
    is_edited = graphene.Boolean()

    class Arguments:
        input = CategoryEditInput(required=True)

    def mutate(self, info, input):
        user = info.context.user
        if not user.is_authenticated and not (user.is_staff or user.is_superuser):
            raise PermissionDenied('You do not have the permission\
             to perform this operation')
        parent = None
        is_edited = False
        if hasattr(input.patch, 'parent'):
            attrs_get = getattr(input.patch, 'parent', None)
            if attrs_get is not None:
                field = dictify_inputs(attrs_get, BaseCategoryInputMixin)
                print(field)
                try:
                    parent = Category.objects.get(
                        id=field['id'] or field['pk'],
                        slug__iexact=field['slug']
                    )
                except Category.DoesNotExist:
                    raise GraphQLError('You are trying to add a parent\
                     category that doesnt exist')
        patch = getattr(input, 'patch')
        patch = dictify_inputs(patch, CategoryPatchInput)
        if 'parent' in patch:
            del patch['parent']
        category = get_object_or_404(Category, id=input.id, slug__iexact=input.slug)
        if category:
            category.parent = parent
            category.name = patch['name']
            category.slug = patch['slug']
            category.description = patch['description']
            category.save(update_fields=['parent', 'name', 'slug', 'description'])
            is_edited = True
        return CategoryEditPayload(category=category, is_edited=is_edited)


class CategoryDeletePayload(graphene.Mutation):
    """
    Deletes a category and returns list of remaining categories.
    Accepts just one parameter called 'input'.
    Must supply 'input' with 'id' and 'slug' of category to be deleted
    """
    categories = graphene.List(CategoryType)
    is_deleted = graphene.Boolean()

    class Arguments:
        input = CategoryDeleteInput(required=True)

    def mutate(self, info, input):
        user = info.context.user
        if not user.is_authenticated and not (user.is_staff or user.is_superuser):
            raise PermissionDenied('You do not have the permission \
            to perform this operation')
        fields = dictify_inputs(input, CategoryDeleteInput)
        category = get_object_or_404(Category, **fields).delete()
        return CategoryDeletePayload(is_deleted=True, categories=Category.objects.all())
