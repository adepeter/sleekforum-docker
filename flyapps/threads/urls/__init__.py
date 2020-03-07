from django.urls import path, include

app_name = 'threads'

urlpatterns = [
    path('<slug:category_slug>/', include('flyapps.threads.urls.thread')),
]