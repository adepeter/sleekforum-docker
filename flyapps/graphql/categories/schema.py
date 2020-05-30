import graphene

from .mutations import CategoryMutations
from .queries import RootCategoryQuery, SubcategoryQueries


class Query(RootCategoryQuery, SubcategoryQueries, graphene.ObjectType):
    pass


class Mutation(CategoryMutations, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
