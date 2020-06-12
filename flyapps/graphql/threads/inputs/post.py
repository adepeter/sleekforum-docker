from django.utils.translation import gettext_lazy as _

import graphene


class ThreadInputMixin(graphene.InputObjectType):
    """Input of thread to which post is attached"""
    id = graphene.ID(
        required=True,
        description=_('ID of thread post belongs to')
    )
    slug = graphene.String(
        required=True,
        description=_('Slug of thread')
    )


class BasePostCreateMixin(graphene.InputObjectType):
    """Input of post"""
    id = graphene.ID
    content = graphene.String(
        required=True,
        description=_('Content of post')
    )


class BasePostEditPatchInput(ThreadInputMixin):
    """Input field for post to be edited"""
    post_id = graphene.ID(
        required=True,
        description=_('ID of post to be modified')
    )


class PostCreateInput(graphene.InputObjectType):
    """Field parameter for new post type to be generated"""
    thread = graphene.InputField(
        ThreadInputMixin,
        required=True,
        description=_('Thread to which post is binded')
    )
    post = graphene.InputField(
        BasePostCreateMixin,
        required=True,
        description=_('Field that holds contents of new post')
    )


class PostEditInput(graphene.InputObjectType):
    """Field paramter for post type to be edited"""
    post = graphene.InputField(
        BasePostEditPatchInput,
        required=True,
        description=_('Field for post to be modified')
    )
    patch = graphene.InputField(
        BasePostCreateMixin,
        description=_('Content to replace post')
    )


class BaseReplyToParentPost(graphene.InputObjectType):
    id = graphene.ID(
        required=True,
        description=_('ID of parent post')
    )
    slug = graphene.String(
        required=True,
        description=_('Slug of parent post thread')
    )


class ReplyToParentPostInput(graphene.InputObjectType):
    parent = graphene.InputField(BaseReplyToParentPost)
    post = graphene.InputField(BasePostCreateMixin)
