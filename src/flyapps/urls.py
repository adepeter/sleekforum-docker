from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'flyapps'

urlpatterns = [
    path('categories/', include('flyapps.categories.urls', namespace='categories')),
    path('graphql/', include('flyapps.graphql.urls', namespace='graphql')),
    path('messages/', include('flyapps.messages.urls', namespace='messages')),
    path('threads/', include('flyapps.threads.urls', namespace='threads')),
    path('users/', include('flyapps.users.urls', namespace='users')),
    path('', include('flyapps.home.urls', namespace='home')),
]
