from django.urls import path
from .. import views

app_name = 'miscs'

urlpatterns = [
    path('search/', views.search, name='search'),
]