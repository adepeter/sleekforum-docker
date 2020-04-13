from django.urls import path, include

from ..views.thread import ListNewestThread, ListTrendingThread

app_name = 'threads'

urlpatterns = [
    path('newest/', ListNewestThread.as_view(), name='newest_threads'),
    path('trending/', ListTrendingThread.as_view(), name='trending_threads'),
]

urlpatterns += [
    path('<slug:category_slug>/', include('flyapps.threads.urls.thread')),
    path('posts/', include('flyapps.threads.urls.post', namespace='post')),
]
