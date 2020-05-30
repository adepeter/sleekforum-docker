import graphene

from .mutations import CategoryMutations
from .queries import CategoryQueries, SubcategoryQueries


class Query(CategoryQueries, SubcategoryQueries, graphene.ObjectType):
    pass


class Mutation(CategoryMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
