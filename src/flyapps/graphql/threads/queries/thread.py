from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

import graphene

from ....threads.models.thread import Thread

from ..types.thread.thread import ThreadType


class ThreadQuery(graphene.ObjectType):
    threads = graphene.List(
        ThreadType,
        category_id=graphene.ID(description=_('ID of category'), required=True),
        category_slug=graphene.String(description=_('Slug of category'), required=True),
        description=_('All threads for a specified category')
    )
    thread = graphene.Field(
        ThreadType,
        category_category=graphene.String(required=True),
        id=graphene.ID(required=True),
        slug=graphene.String(required=True)
    )

    def resolve_threads(self, info, category_id, category_slug):
        return Thread.objects.filter(
            category__id=category_id,
            category__slug__iexact=category_slug
        )

    def resolve_thread(self, info, category_slug, id, slug):
        return get_object_or_404(
            Thread,
            category__slug__iexact=category_slug,
            id=id,
            slug__iexact=slug
        )
