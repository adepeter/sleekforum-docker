from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _

from ..forms.profile import UserSearchForm, UserProfileEditForm

TEMPLATE_URL = 'flyapps/users/profile'
User = get_user_model()


class UserSearch(FormMixin, ListView):
    model = User
    form_class = UserSearchForm
    template_name = f'{TEMPLATE_URL}/user_search.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class UserProfile(DetailView):
    model = User
    template_name = f'{TEMPLATE_URL}/user_profile.html'

    def get_object(self):
        obj = get_object_or_404(User, slug__iexact=self.request.user.username)
        if self.kwargs.get('slug'):
            obj = super().get_object()
        return obj


class UserProfileEdit(SuccessMessageMixin, UpdateView):
    """WOuld implement this view when i get a better template"""
    model = User
    form_class = UserProfileEditForm
    template_name = f'{TEMPLATE_URL}/user_profile_edit.html'
    success_url = reverse_lazy('flyapps:users:profile:home_profile')
    success_message = _('Profile successfully updated')


class UserProfileDelete(DeleteView):
    model = User
    success_url = reverse_lazy('flyapps:home')
 
@require_POST
def profile_edit(request, slug):
    user = get_object_or_404(User, slug__iexact=slug)
    form = UserProfileEditForm(data=request.POST, file=request.FILES)
    if form.has_changed():
        if form.is_valid():
            pass