import graphene

from .thread import ThreadQuerySchema, ThreadMutationSchema
from .post import PostQuerySchema


class Query(ThreadQuerySchema, PostQuerySchema, graphene.ObjectType):
    pass


class Mutation(ThreadMutationSchema, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
