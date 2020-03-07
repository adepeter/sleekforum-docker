from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from ..forms.register import UserRegistrationForm


TEMPLATE_URL = 'flyapps/users/auth'

User = get_user_model()

def register_user(request):
    template_name = f'{TEMPLATE_URL}/register.html'
    registration_successful = False
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            email = cleaned_data['email']
            username = cleaned_data['username']
            password = cleaned_data['password_1']
            new_user = User.objects.create_user(email, username, password)
            if new_user:
                messages.success(request, _('Registration was successfull'))
                registration_successful = True
    else:
        form = UserRegistrationForm()
    return render(request, template_name, {
        'form': form,
        'registration_successful': registration_successful
    })