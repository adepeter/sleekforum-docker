from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from ..rules.fields import RulesModelMultipleChoiceFieldWithId
from ..rules.models import Rule

from .models import Violation


class BaseViolationForm(forms.ModelForm):
    allowed_categories = None
    rules = RulesModelMultipleChoiceFieldWithId(queryset=None)

    class Meta:
        model = Violation
        fields = ['rules']

    def __init__(self, *args, **kwargs):
        self.object = kwargs.pop('object')
        self.request = kwargs.pop('request')
        self.queryset = self.get_allowed_rule_categories()
        super().__init__(*args, **kwargs)
        self.fields['rules'] = RulesModelMultipleChoiceFieldWithId(
            queryset=self.repeat_reported_rules(),
            widget=forms.CheckboxSelectMultiple
        )

    def get_allowed_rule_categories(self):
        if self.allowed_categories is None:
            raise ImproperlyConfigured(
                _('You must set an allowed_category attribute on your form')
            )
        return Rule.objects.filter(category__in=self.allowed_categories)

    def clean_rules(self):
        cleaned_rules = self.cleaned_data['rules']
        check_spam_violations = self.check_spam_rules(cleaned_rules, self.request.user)
        if check_spam_violations:
            raise forms.ValidationError(
                _('A rule cannot be reported twice for violation'), code='multiple_violations'
            )
        return cleaned_rules

    """
    This method is called to ensure a report action is not repeated twice.
    If repeat_reported_rule() is set to false, this method have no use.
    """

    def check_spam_rules(self, rules, user):
        violations = Violation.objects.filter(
            content_type=self.get_content_type_for_object,
            object_id=self.object.id,
            user=user,
            rules__in=rules
        )
        return violations.exists()

    """
    Always use this method in subclasses to return queryset.
    Do not set queryset directly on fields
    """
    def repeat_reported_rules(self, repeat_rule=True):
        if repeat_rule:
            return self.queryset
        return self.unique_rules_queryset

    @property
    def get_content_type_for_object(self):
        return ContentType.objects.get_for_model(self.object)

    @property
    def unique_rules_queryset(self):
        return self.queryset.exclude(
            violations__isnull=False,
            violations__is_violated__in=[Violation.PENDING, Violation.ACCEPT],
            violations__content_type=self.get_content_type_for_object,
            violations__object_id=self.object.id,
            violations__user=self.request.user
        )
