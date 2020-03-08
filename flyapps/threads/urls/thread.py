from django.urls import path, include
from ..views.thread import (
    ListThread,
    CreateThread,
    ReadThread,
    EditThread,
    DeleteThread
)
from ..views.thread_misc import (
    HideThread,
    LockThread,
    ShareThread,
    ReportThread,
    UnhideThread,
    UnlockThread
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

# Admin actions
urlpatterns += [
    path('<int:pk>/<slug:slug>/hide/', HideThread.as_view(), name='hide_thread'),
    path('<int:pk>/<slug:slug>/lock/', LockThread.as_view(), name='lock_thread'),
    path('<int:pk>/<slug:slug>/unhide/', UnhideThread.as_view(), name='unhide_thread'),
    path('<int:pk>/<slug:slug>/unlock/', UnlockThread.as_view(), name='unlock_thread'),
]

# Misc actions
urlpatterns += [
    path('<int:pk>/<slug:slug>/share/', ShareThread.as_view(), name='share_thread'),
    path('<int:pk>/<slug:slug>/report/', ReportThread.as_view(), name='report_thread'),
]

# Dirty hack for Posts (IE comments) URL inclusion
urlpatterns += [
    path('', include('flyapps.threads.urls.post', namespace='post')),
]
