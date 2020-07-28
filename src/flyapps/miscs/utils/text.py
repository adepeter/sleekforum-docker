from django.utils.crypto import get_random_string


def generate_random_string(length=10, allow_special_chars=True):
    allowed_chars = 'abcdefghijklmnopqrstuvwxyz' \
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    if allow_special_chars:
        special_chars = "\"!@#\\$%^&*()_+~{}:?<>`-[];'/"
        allowed_chars += special_chars
    return get_random_string(length, allowed_chars)


def truncator(obj, word_count=20, completer='...'):
    splitted_text = obj.split()
    if len(splitted_text) > word_count:
        obj = ' '.join((splitted_text)[:word_count]).rstrip()
        return '{0} {1}'.format(obj, completer)
    return obj


class Textifier:
    def __init__(self, text):
        self.text = text or None
        super().__init__(text)

    @staticmethod
    def random_string(self, length=10, allow_special_chars=False):
        self.text = generate_random_string(length, allow_special_chars)
        return self.text
