from .models import Reply

def get_last_reply_for_message(message):
    """
    This is a shortcut function to get latest reply for a message
    If reply does not exist, it returns the message
    """
    try:
        obj = message.replies.latest('created')
    except Reply.DoesNotExist:
        obj = message
    return obj