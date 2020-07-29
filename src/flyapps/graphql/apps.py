from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class GraphqlConfig(AppConfig):
    name = 'flyapps.graphql'
    label = 'flyapps_graphql'
    verbose_name = _('Sleekforum GraphQL')
    models_module = None
