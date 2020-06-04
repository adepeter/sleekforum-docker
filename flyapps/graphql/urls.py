from django.urls import include, path

app_name = 'graphql'

urlpatterns = [
    path('categories/', include('flyapps.graphql.categories.urls', namespace='categories')),
    # path('threads/', include('flyapps.graphql.threads.urls', namespace='threads')),
    path('users/', include('flyapps.graphql.users.urls', namespace='users')),
]