from django.shortcuts import render
from django.contrib.auth.views import LoginView
from ..forms.auth import AuthenticationForm

TEMPLATE_URL = 'flyapps/users/auth'


class AuthLogin(LoginView):
    template_name = f'{TEMPLATE_URL}/login.html'
    form_class = AuthenticationForm

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(self.request, f'{TEMPLATE_URL}/session_active.html')
        return super(AuthLogin, self).get(*args, **kwargs)
