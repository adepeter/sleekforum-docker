from django.urls import path, include

from ..views.statistic import UserList

app_name = 'users'

urlpatterns = [
    path('statistics/', UserList.as_view(), name='users_list'),
]
urlpatterns += [
    path('auth/', include('flyapps.users.urls.auth', namespace='auth')),
    path('profile/', include('flyapps.users.urls.profile', namespace='profile')),
]
