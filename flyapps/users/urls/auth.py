from django.urls import path
from ..views import auth, register

app_name = 'auth'

urlpatterns = [
    path('login/', auth.AuthLogin.as_view(), name='login'),
    path('logout/', auth.AuthLogout.as_view(), name='logout'),
    path('register/', register.UserRegistration.as_view(), name='register'),
]
