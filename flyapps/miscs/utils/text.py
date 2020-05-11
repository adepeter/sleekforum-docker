from django.utils.crypto import get_random_string


def generate_random_string(length=10, allow_special_chars=True):
    allowed_chars = 'abcdefghijklmnopqrstuvwxyz' \
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    if allow_special_chars:
        special_chars = "\"!@#\\$%^&*()_+~{}:?<>`-[];'/"
        allowed_chars += special_chars
    return get_random_string(length, allowed_chars)


class Textifier:
    def __init__(self, text):
        self.text = text or None
        super().__init__(text)

    @staticmethod
    def random_string(self, length=10, allow_special_chars=False):
        self.text = generate_random_string(length, allow_special_chars)
        return self.text
