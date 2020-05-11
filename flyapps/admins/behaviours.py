from django.db import models, ProgrammingError


class ConfigurationSingletonMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

    def delete(self, *args, **kwargs):
        try:
            if self.id != 1:
                super().delete(*args, **kwargs)
        except ProgrammingError:
            """This prevents deletion of object"""
            pass
