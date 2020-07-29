from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormView

from ..forms.register import UserRegistrationForm

TEMPLATE_URL = 'flyapps/users/auth'

User = get_user_model()


class UserRegistration(SuccessMessageMixin, FormView):
    form_class = UserRegistrationForm
    success_message = _('Registration was successful')
    template_name = f'flyapps/users/auth/register.html'
    success_url = reverse_lazy('flyapps:home:home')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return render(self.request, f'{TEMPLATE_URL}/session_active.html')
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
