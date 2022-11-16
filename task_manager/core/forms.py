from .models import Status, Task, Label
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name', ]


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class LabelForm(ModelForm):

    class Meta:
        model = Label
        fields = ['name', ]


class TaskFilter(forms.Form):
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False)
    executor = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    label = forms.ModelChoiceField(queryset=Label.objects.all(), required=False)
    self_tasks = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
    )
