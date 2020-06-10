from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import graphene

from ....categories.models import Category

from ....threads.models.thread import Thread

from ...utils import DictifyNestedInput as DictifyInput

from ..inputs.thread import (
    ThreadCreateInput,
    ThreadDeleteInput,
    ThreadEditInput,
)
from ..types.thread.thread import ThreadType


class ThreadCreatePayload(graphene.Mutation):
    """Payload for creating new thread"""
    thread = graphene.Field(
        ThreadType,
        description=_('Newly created thread type')
    )

    class Arguments:
        input = ThreadCreateInput(
            description=_('New thread inputs'),
            required=True
        )

    def mutate(self, info, input):
        user = info.context.user
        dictifier = DictifyInput(input)
        serialize_category = dictifier.get_fields_or_field('category')
        serialize_thread = dictifier.get_fields_or_field('thread')
        if 'tags' in serialize_thread:
            serialize_thread.update({
                'tags': [slugify(x) for x in serialize_thread['tags']]
            })
        category = get_object_or_404(Category, **serialize_category)
        if not user.is_authenticated:
            raise PermissionDenied(_('You cannot perform this operation'))
        thread = category.threads.create(starter=user, **serialize_thread)
        return ThreadCreatePayload(thread=thread)


class ThreadEditPayload(graphene.Mutation):
    """Payload for updating exiting thread"""
    thread = graphene.Field(
        ThreadType,
        description=_('Edited thread'),
        required=True
    )

    class Arguments:
        input = ThreadEditInput(
            description=_('thread type to edit'),
            required=True,
        )

    def mutate(self, info, input):
        input = DictifyInput(input)
        thread = input.get_fields_or_field('thread')
        patch = input.get_fields_or_field('patch')
        category_slug = thread.pop('category_slug')
        obj = get_object_or_404(
            Thread,
            category__slug__iexact=category_slug,
            **thread
        )
        if patch is not None:
            if 'category' in patch:
                category = get_object_or_404(Category, **patch['category'])
            for k, v in patch['thread'].items():
                setattr(obj, k, v)
            obj.category = category
            obj.slug = slugify(obj.slug)
            obj.save()
        return ThreadEditPayload(thread=obj)

class ThreadDeletePayload(graphene.Mutation):
    """Payload for thread deletion"""
    threads = graphene.List(
        ThreadType,
        description=_('List of threads in same category after deletion')
    )
    thread = graphene.Field(
        ThreadType,
        description=_('Thread to delete')
    )
    is_deleted = graphene.Boolean(
        description=_('Confirmation whether thread is deleted'),
        required=True
    )
    
    class Arguments:
        input = ThreadDeleteInput(
            description=_('thread type to delete'),
            required=True
        )
    
    def mutate(self, info, input):
        thread = get_object_or_404(
            Thread,
            category__slug__iexact=input.category_slug,
            id=input.id,
            slug__iexact=input.slug
        )
        threads = Thread.objects.filter(
            category__slug=input.category_slug
        )
        if not info.context.user.is_superuser:
            return ThreadDeletePayload(
                threads=threads,
                thread=thread,
                is_deleted=False
            )
        else:
            thread.delete()
            return ThreadDeletePayload(
                threads=threads,
                is_deleted=True
            )