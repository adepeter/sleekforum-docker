from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from .schema import schema

app_name = 'categories'

urlpatterns = [
    path('', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name='categories_graphql'),

]
