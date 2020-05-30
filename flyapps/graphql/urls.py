from django.urls import include, path

app_name = 'graphql'

urlpatterns = [
    path('categories/', include('flyapps.graphql.categories.urls', namespace='categories')),
]