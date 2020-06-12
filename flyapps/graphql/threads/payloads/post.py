from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

import graphene

from ....threads.models.thread import Thread
from ....threads.models.post import Post

from ...utils import DictifyNestedInput as DictifyInput

from ..inputs.post import (
    PostCreateInput,
    PostEditInput
)
from ..types.post import PostType


class PostCreatePayload(graphene.Mutation):
    post = graphene.Field(
        PostType,
        description=_('Newly created post object type')
    )
    is_created = graphene.Boolean(
        default_value=False,
        description=_('Boolean value to confirm if new post is created')
    )

    class Arguments:
        input = PostCreateInput(
            required=True,
            description=_('New post type')
        )

    def mutate(self, info, input):
        user = info.context.user
        if not user.is_authenticated:
            raise PermissionDenied('You cannot perform this operation')
        input = DictifyInput(input)
        serialize_thread = input.get_fields_or_field('thread')
        serialize_post = input.get_fields_or_field('post')
        thread = get_object_or_404(Thread, **serialize_thread)
        post = thread.posts.create(user=user, **serialize_post)
        return PostCreatePayload(post=post, is_created=True)


class PostEditPayload(graphene.Mutation):
    post = graphene.Field(
        PostType,
        description=_('Edited post object type')
    )
    is_edited = graphene.Boolean(
        description=_('Confirmation if post was successfully edited'),
        default_value=False
    )

    class Arguments:
        input = PostEditInput(
            required=True,
            description=_('Post to be edited'),
        )
        
    def mutate(self, info, input):
        input = DictifyInput(input)
        # serialize_post = input.get_fields_or_field('post').pop('id')
        # post = get_object_or_404(
        #     Post,
        #     thread__slug__iexact=
        #     **serialize_post
        # )