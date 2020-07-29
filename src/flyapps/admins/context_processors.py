from .models import BaseConfiguration


def site_configurations(request):
    return {'configurations': BaseConfiguration.load()}
