from django.shortcuts import get_list_or_404, get_object_or_404

from ....threads.models import Post

import graphene

from ....threads.models.thread import Thread

from ..types.post.post import PostType

class SingleThreadObjectType:
    category_slug = graphene.String()
    id = graphene.ID()
    slug = graphene.String()

class PostQuery(graphene.ObjectType):
    posts = graphene.List(
        PostType,
        category_slug=graphene.String(),
        id=graphene.ID(),
        slug=graphene.String()
    )

    def resolve_posts(self, info, category_slug, id, slug, **kwargs):
        thread = get_object_or_404(
            Thread,
            category__slug__iexact=category_slug,
            id=id,
            slug__iexact=slug
        )
        return thread.posts.all()
