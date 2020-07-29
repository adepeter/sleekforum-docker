from django.contrib.auth import get_user_model
from django.views.generic import ListView

TEMPLATE_URL = 'flyapps/users/statistic'

User = get_user_model()

class UserList(ListView):
    template_name = f'{TEMPLATE_URL}/users_list.html'
    context_object_name = 'users'
    paginate_by = 10
    ordering = ['username']

    def get_queryset(self):
        return User.objects.filter(is_active=True)