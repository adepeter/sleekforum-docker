from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import graphene

from ....categories.models import Category

from ...utils import DictifyInput

from ..inputs.thread import ThreadCreateInput
from ..types.thread.thread import ThreadType


class ThreadCreatePayload(graphene.Mutation):
    thread = graphene.Field(ThreadType)

    class Arguments:
        input = ThreadCreateInput()

    def mutate(self, info, input):
        user = info.context.user
        dictifier = DictifyInput(input)
        serialize_category = dictifier.get_fields_or_field('category')
        serialize_thread = dictifier.get_fields_or_field('thread')
        if 'tags' in serialize_thread:
            serialize_thread.update({
                'tags': [slugify(x) for x in serialize_thread['tags']]
            })
        print(serialize_thread)
        # category = get_object_or_404(Category, **serialize_category)
        # if not user.is_authenticated:
        #     raise PermissionDenied(_('You cannot perform this operation'))
        # thread = category.threads.create(starter=user, **serialize_thread)
        # return ThreadCreatePayload(thread=thread)
