from django.urls import path
from ..views.post import (
    EditPost
)

app_name = 'post'

urlpatterns = [
    path('<slug:thread_slug>/<int:pk>/edit_comment/', EditPost.as_view(), name='edit_post'),
]
