from django.urls import path

from .views import InboxMessage, ReadReplyMessage, StartMessage

app_name = 'messages'

urlpatterns = [
    path('', InboxMessage.as_view(), name='new_inbox'),
    path('<int:pk>/', ReadReplyMessage.as_view(), name='read_reply_message'),
    path('<int:pk>/<slug:starter>/', ReadReplyMessage.as_view(), name='read_reply_message'),
    path('<slug:recipient>/compose/', StartMessage.as_view(), name='start_message'),
]