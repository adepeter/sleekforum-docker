from django.urls import path
from ..views.post import (
    EditPost,
    DeletePost
)

app_name = 'post'

urlpatterns = [
    path('<slug:thread_slug>/<int:pk>/edit_post/', EditPost.as_view(), name='edit_post'),
    path('<slug:thread_slug>/<int:pk>/delete_post/', DeletePost.as_view(), name='delete_post'),
]
