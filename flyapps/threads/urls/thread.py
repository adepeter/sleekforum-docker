from django.urls import path, include

from ..views.thread import (
    ListThread,
    CreateThread,
    ReadThread,
    EditThread,
    DeleteThread
)
from ..views.thread.thread_misc import (
    SearchThread,
    ShareThread,
    ReportThread,
    LockUnlockThread,
    HideUnhideThread,
    LikeThread,
    DislikeThread,
)

urlpatterns = [
    path('', ListThread.as_view(), name='list_threads'),
    path('create/', CreateThread.as_view(), name='create_thread'),
    path('search/', SearchThread.as_view(), name='search_thread'),
]

urlpatterns += [
    path('<int:pk>/<slug:slug>/', include([
        path('', ReadThread.as_view(), name='read_thread'),
        path('edit/', EditThread.as_view(), name='edit_thread'),
        path('delete/', DeleteThread.as_view(), name='delete_thread'),
        path('share/', ShareThread.as_view(), name='share_thread'),
        path('report/', ReportThread.as_view(), name='report_thread'),
        path('hide-unhide/', HideUnhideThread.as_view(), name='toggle_hide_thread'),
        path('lock-unlock/', LockUnlockThread.as_view(), name='toggle_lock_thread'),
        path('like/', LikeThread.as_view(), name='like_thread'),
        path('dislike/', DislikeThread.as_view(), name='dislike_thread'),
    ])),
]
