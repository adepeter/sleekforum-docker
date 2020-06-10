from django.views.decorators.csrf import csrf_exempt
from django.urls import path

from graphene_django.views import GraphQLView

from .schemas import schema

app_name = 'threads'

urlpatterns = [
    path(
        '',
        csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)),
        name='threads_graphql'
    )
]
