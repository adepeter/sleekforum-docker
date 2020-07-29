from .models import Message


def inbox(request):
    user = request.user
    messages = user.messages_received.exclude(flag=Message.FLAG_ACTIVE)
    return {'inbox': messages}
