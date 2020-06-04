import graphene

from .mutations import CategoryMutation
from .queries import CategoryQuery


class Mutation(CategoryMutation, graphene.ObjectType):
    pass


class Query(CategoryQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
