from django.urls import path, include

from .views.base import Homepage
from .views.pages import ContactUs, GlobalSearch, GlobalStatistics

app_name = 'home'

urlpatterns = [
    path('', Homepage.as_view(), name='home'),
]

urlpatterns += [
    path('pages/', include([
        path('contact-us/', ContactUs.as_view(), name='contact_us'),
        path('search/', GlobalSearch.as_view(), name='global_search'),
        path('statistics/', GlobalStatistics.as_view(), name='global_statistics'),
    ]))
]