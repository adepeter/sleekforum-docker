from django.conf import settings
from django.db import models
from django.utils import timezone

from .thread import Thread


class ThreadRule(models.Model):
    rule = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    show_rule = models.BooleanField(default=True)


class ThreadReport(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_reports')
    reported_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='thread_reports')
    rules_broken = models.ManyToManyField(ThreadRule, related_name='thread_reports')
    reported_on = models.DateTimeField(default=timezone.now)
