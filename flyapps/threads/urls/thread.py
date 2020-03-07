from django.urls import path, include
from ..views.thread import (
    ListThread,
    CreateThread,
    ReadThread,
    EditThread,
    DeleteThread,
    ShareThread,
)

urlpatterns = [
    path('', ListThread.as_view(), name='list_threads'),
    path('create/', CreateThread.as_view(), name='create_thread'),
]

urlpatterns += [
    path('<int:pk>/<slug:slug>/', ReadThread.as_view(), name='read_thread'),
    path('<int:pk>/<slug:slug>/edit/', EditThread.as_view(), name='edit_thread'),
    path('<int:pk>/<slug:slug>/delete', DeleteThread.as_view(), name='delete_thread'),
]

# Dirty hack for Posts URL inclusion
urlpatterns += [
    path('', include('flyapps.threads.urls.post', namespace='post')),
]

urlpatterns += [
    path('<int:pk>/<slug:slug>/share/', ShareThread.as_view(), name='share_thread'),

]
