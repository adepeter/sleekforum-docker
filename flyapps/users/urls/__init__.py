from django.urls import path, include
from ..views.auth import AuthLogin

app_name = 'users'

urlpatterns = [
    path('auth/', include('flyapps.users.urls.auth', namespace='auth')),
    path('profile/', include('flyapps.users.urls.profile', namespace='profile')),
]