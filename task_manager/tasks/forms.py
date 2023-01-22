from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils.translation import pgettext

from task_manager.labels.models import Label
from task_manager.statuses.models import Status

from task_manager.tasks.models import Task


class UserModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.get_full_name()


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        field_classes = {'executor': UserModelChoiceField}


class TaskFilter(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label=pgettext('Status filter', 'Status')
    )
    executor = UserModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=pgettext('Executor filter', 'Executor')
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=pgettext('Label filter', 'Label')
    )
    self_tasks = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
        label=pgettext('Self tasks filter', 'Self tasks')
    )
