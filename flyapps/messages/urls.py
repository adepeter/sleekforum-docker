from django.urls import include, path

from .views import InboxMessage, ReplyMessage, StartMessage

app_name = 'messages'

urlpatterns = [
    path('', InboxMessage.as_view(), name='new_inbox'),
]

urlpatterns += [
    path('<slug:recipient>/', include([
        path('<int:pk>/', ReplyMessage.as_view(), name='reply_message'),
        path('start/', StartMessage.as_view(), name='start_message'),
    ]))
]
