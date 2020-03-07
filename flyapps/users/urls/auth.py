from django.urls import path
from ..views import auth, register

app_name = 'auth'

urlpatterns = [
    path('login/', auth.AuthLogin.as_view(), name='login'),
    path('register/', register.register_user, name='register'),
]