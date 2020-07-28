import graphene

from .thread import ThreadQuerySchema, ThreadMutationSchema
from .post import PostQuerySchema, PostMutationSchema


class Query(ThreadQuerySchema, PostQuerySchema, graphene.ObjectType):
    """Queries for threads app"""


class Mutation(ThreadMutationSchema, PostMutationSchema, graphene.ObjectType):
    """Mutations for threads app"""


schema = graphene.Schema(query=Query, mutation=Mutation)
