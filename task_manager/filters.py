import django_filters
from django_filters.filters import ModelChoiceFilter
from django.contrib.auth.models import User
from django.utils.translation import pgettext
from django import forms

from .models import Task, Status, Label


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class UserModelChoiceFilter(ModelChoiceFilter):
    field_class = UserModelChoiceField


class TaskFilter(django_filters.FilterSet):

    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all()
    )
    executor = UserModelChoiceFilter(
        queryset=User.objects.all()
    )
    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        label=pgettext('Label filter', 'Label'),
        field_name='labels',
    )
    # self_tasks = django_filters.BooleanFilter(
    #     label=pgettext('Self tasks filter', 'Self tasks'),
    #     widget=forms.CheckboxInput,
    #     # field_name='author',
    # )

    # class Meta:
    #     model = Task
    #     fields = ['status', 'executor', 'label', 'self_tasks']
