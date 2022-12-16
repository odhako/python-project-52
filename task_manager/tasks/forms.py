from django import forms
from django.forms import ModelForm

from task_manager.models import Task


class UserModelChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        return obj.get_full_name()


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        field_classes = {'executor': UserModelChoiceField}
