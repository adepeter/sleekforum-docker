from django.urls import include, path
from ..views.post import (
    EditPost,
    DeletePost,
    ReplyPost
)
from ..views.post.post_misc import UpVotePost

app_name = 'post'

urlpatterns = [
    path('<slug:thread_slug>/<int:pk>/', include([
        path('edit/', EditPost.as_view(), name='edit_post'),
        path('delete_post/', DeletePost.as_view(), name='delete_post'),
        path('reply/', ReplyPost.as_view(), name='reply_post'),
        path('upvote/', UpVotePost.as_view(), name='upvote_post'),
    ])),
]
