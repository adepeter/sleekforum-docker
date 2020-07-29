from django.db import models


class RoleManager(models.Manager):
    """
    The manager for the role model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)
