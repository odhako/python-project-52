from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Task, Label
from .statuses.models import Status
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.utils.translation import pgettext


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


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )


class UserLoginForm(AuthenticationForm):
    pass
