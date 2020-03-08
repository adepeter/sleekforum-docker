from django.urls import path, include
from django.views.generic import TemplateView

app_name = 'flyapps'


def home(request):
    from django.http import HttpResponse
    return HttpResponse('welcome')


urlpatterns = [
    path('home/', home, name='home'),
    path('categories/', include('flyapps.categories.urls', namespace='categories')),
    path('threads/', include('flyapps.threads.urls', namespace='threads')),
    path('miscs/', include('flyapps.miscs.urls', namespace='miscs')),
    path('users/', include('flyapps.users.urls', namespace='users')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
