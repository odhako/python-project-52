from .models import Status, Task, Label
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class NoLabelSuffixMixin:
    def __init__(self, *args, **kwargs):
        if 'label_suffix' not in kwargs:
            kwargs['label_suffix'] = ''
        super().__init__(*args, **kwargs)


class PlaceholderMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_names = [field_name for field_name, _ in self.fields.items()]
        for field_name in field_names:
            field = self.fields.get(field_name)
            field.widget.attrs.update({'placeholder': field.label})


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'


class StatusForm(NoLabelSuffixMixin,
                 PlaceholderMixin,
                 FormControlMixin,
                 ModelForm):
    class Meta:
        model = Status
        fields = ['name', ]


class TaskForm(NoLabelSuffixMixin,
               PlaceholderMixin,
               FormControlMixin,
               ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']


class LabelForm(NoLabelSuffixMixin,
                PlaceholderMixin,
                FormControlMixin,
                ModelForm):

    class Meta:
        model = Label
        fields = ['name', ]


class TaskFilter(NoLabelSuffixMixin, FormControlMixin, forms.Form):
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=False)
    executor = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    label = forms.ModelChoiceField(queryset=Label.objects.all(), required=False)
