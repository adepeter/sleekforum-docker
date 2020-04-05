from django.urls import path, include

from ..views.profile import UserProfile, UserProfileEdit, UserProfileDelete

app_name = 'profile'

urlpatterns = [
    path('', UserProfile.as_view(), name='home_profile'),
]

urlpatterns += [
    path('<slug:slug>/', include([
        path('', UserProfile.as_view(), name='user_profile'),
        path('edit/', UserProfileEdit.as_view(), name='user_profile_edit'),
        path('delete/', UserProfileDelete.as_view(), name='user_profile_delete'),
    ])),
]
