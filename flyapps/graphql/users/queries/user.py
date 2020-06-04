from django.contrib.auth import get_user_model

import graphene

from ..types.user import UserType

User = get_user_model()


class UserQuery:
    user = graphene.Field(UserType, slug=graphene.String())
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_me(self, info, **kwargs):
        user = info.context.user
        return User.objects.get(slug=user.slug)

    def resolve_user(self, info, slug):
        return User.objects.get(slug__iexact=slug)
