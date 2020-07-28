from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse

from ..forms.auth import PasswordResetForm, SetPasswordForm

TEMPLATE_URL = 'flyapps/users/auth/password'


class AuthPasswordReset(PasswordResetView):
    success_url = reverse_lazy('flyapps:users:auth:password_reset_done')
    subject_template_name = '%s/password_reset_subject.txt' % TEMPLATE_URL
    email_template_name = '%s/password_reset_email.html' % TEMPLATE_URL
    form_class = PasswordResetForm
    template_name = f'{TEMPLATE_URL}/forgot_password.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('flyapps:home:home'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.session['password_reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)


class AuthPasswordResetDone(PasswordResetDoneView):
    template_name = f'{TEMPLATE_URL}/password_reset_done.html'

    def get(self, request, *args, **kwargs):
        if request.session.get('password_reset_email') is None:
            return HttpResponseRedirect(reverse('flyapps:home:home'))
        self.session_pop = request.session.pop('password_reset_email')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email'] = self.session_pop
        return context


class AuthPasswordResetConfirm(PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = f'{TEMPLATE_URL}/password_reset_confirm.html'

    def form_valid(self, form):
        self.request.session['pass_reset_complete'] = True
        return super().form_valid(form)

class AuthPasswordResetComplete(PasswordResetCompleteView):
    template_name = f'{TEMPLATE_URL}/password_reset_complete.html'

    def get(self, request, *args, **kwargs):
        self.pass_reset_complete = self.get_session()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_reset_complete'] = self.pass_reset_complete
        return context

    def get_session(self):
        try:
            return self.request.session.pop('password_reset_complete')
        except KeyError:
            return False