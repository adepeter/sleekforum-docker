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
    path('<int:pk>/<slug:slug>/', include([
        path('', ReadThread.as_view(), name='read_thread'),
        path('edit/', EditThread.as_view(), name='edit_thread'),
        path('delete/', DeleteThread.as_view(), name='delete_thread'),
        path('share/', ShareThread.as_view(), name='share_thread'),
        path('report/', ReportThread.as_view(), name='report_thread'),
        path('hide/', HideThread.as_view(), name='hide_thread'),
        path('lock/', LockThread.as_view(), name='lock_thread'),
        path('unhide/', UnhideThread.as_view(), name='unhide_thread'),
        path('unlock/', UnlockThread.as_view(), name='unlock_thread'),
    ])),
]

# Dirty hack for Posts (IE comments) URL inclusion
urlpatterns += [
    path('', include('flyapps.threads.urls.post', namespace='post')),
]
