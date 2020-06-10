import graphene

from .thread import ThreadQuerySchema, ThreadMutationSchema
from .post import PostQuerySchema


class Query(ThreadQuerySchema, PostQuerySchema, graphene.ObjectType):
    """Queries for threads app"""


class Mutation(ThreadMutationSchema, graphene.ObjectType):
    """Mutations for threads app"""


schema = graphene.Schema(query=Query, mutation=Mutation)
