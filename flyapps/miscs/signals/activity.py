from django.dispatch import Signal

activity_updater = Signal(providing_args=['action_value', 'obj'])
