from django.urls import path
from ..views import auth, password, register

app_name = 'auth'

urlpatterns = [
    path('login/', auth.AuthLogin.as_view(), name='login'),
    path('logout/', auth.AuthLogout.as_view(), name='logout'),
    path('password-reset/', password.AuthPasswordReset.as_view(), name='password_reset'),
    path('password-reset/<uidb64>/<token>/', password.AuthPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('password-reset-done/', password.AuthPasswordResetDone.as_view(), name='password_reset_done'),
    path('register/', register.UserRegistration.as_view(), name='register'),
]
