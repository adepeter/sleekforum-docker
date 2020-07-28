from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..miscs.fields import CommaSeparatedField

from .behaviours import ConfigurationSingletonMixin

# Create your models here.

class MetaTag(models.Model):
    meta_author = models.TextField()
    meta_keywords = CommaSeparatedField()
    meta_description = models.TextField()
    

class ItemPerPageConfiguration(ConfigurationSingletonMixin):
    site_users_per_page = models.PositiveSmallIntegerField()
    site_users_per_admin_page = models.PositiveSmallIntegerField()
    site_posts_per_thread = models.PositiveSmallIntegerField()
    site_threads_per_page = models.PositiveSmallIntegerField()
    
class URLConfiguration(ConfigurationSingletonMixin):
    site_email = models.EmailField()
    site_github = models.URLField()
    site_facebook = models.URLField()
    site_twitter = models.URLField()

class BaseConfiguration(ConfigurationSingletonMixin):
    site_url = models.URLField()
    site_use_logo = models.BooleanField(default=False)
    site_logo = models.ImageField()
    site_name = models.CharField()
    site_index_title = models.CharField()
    site_under_maintainance = models.BooleanField(default=False)
    
    
class UserRank(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField()
    items = JSONField()