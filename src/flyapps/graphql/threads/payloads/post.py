from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

import graphene

from ....threads.models.thread import Thread
from ....threads.models.post import Post

from ...utils import DictifyNestedInput as DictifyInput

from ..inputs.post import (
    PostCreateInput,
    PostEditInput,
    PostDeleteInput
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
        serialize_post = input.get_fields_or_field('post')
        post = get_object_or_404(
            Post,
            id=serialize_post['post_id'],
            thread__id=serialize_post['id'],
            thread__slug__iexact=serialize_post['slug'],
        )
        serialize_patch = input.get_fields_or_field('patch')
        if not info.context.user.is_authenticated:
            raise PermissionDenied(
                _('You do not have permision to complete this operation.')
            )
        post.content = serialize_patch['content']
        post.save(update_fields=['content'])
        return PostEditPayload(post=post, is_edited=True)


class PostDeletePayload(graphene.Mutation):
    posts = graphene.List(
        PostType,
        description=_('List of remaining posts on a thread')
    )
    is_deleted = graphene.Boolean(
        default_value=False,
        description=_('Confirmation of post as deleted')
    )

    class Arguments:
        input = PostDeleteInput(
            required=True,
            description=_('Post to be deleted')
        )

    def mutate(self, info, input):
        post = get_object_or_404(
            Post,
            thread__id=input.id,
            thread__slug__iexact=input.slug,
            id=input.post_id
        )
        if not info.context.user.is_superuser:
            raise PermissionDenied(
                _('You are not authorized to delete this post')
            )
        posts = Post.objects.filter(
            thread__id=input.id,
            thread__slug__iexact=input.slug
        )
        post.delete()
        return PostDeletePayload(posts=posts, is_deleted=True)
