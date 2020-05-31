import graphene

from .mutations import CategoryMutations
from .queries import RootCategoryQuery


class Query(RootCategoryQuery, graphene.ObjectType):
    pass


class Mutation(CategoryMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
