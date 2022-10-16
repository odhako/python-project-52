from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NoLabelSuffixMixin:
    def __init__(self, *args, **kwargs):
        if 'label_suffix' not in kwargs:
            kwargs['label_suffix'] = ''
        super(NoLabelSuffixMixin, self).__init__(*args, **kwargs)


class PlaceholderMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_names = [field_name for field_name, _ in self.fields.items()]
        for field_name in field_names:
            field = self.fields.get(field_name)
            field.widget.attrs.update({'placeholder': field.label})


class UserRegistrationForm(NoLabelSuffixMixin, PlaceholderMixin, UserCreationForm):
    #
    # label_suffix = ''
    # # email = forms.EmailField(required=True)
    # first_name = forms.CharField(
    #     label=_("First name"),
    #     max_length=150,
    #     # label_suffix='',
    #     required=True,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'required': '',
    #         'placeholder': _("First name"),
    #     })
    # )
    #
    # last_name = forms.CharField(
    #     label=_("Last name"),
    #     max_length=150,
    #     label_suffix='',
    #     required=True,
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'required': '',
    #         'placeholder': _("Last name"),
    #     })
    # )
    #
    # username = forms.CharField(
    #     label=_("Username"),
    #     max_length=150,
    #     label_suffix='',
    #     required=True,
    #     help_text=_(
    #         "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    #     ),
    #     error_messages={
    #         "unique": _("A user with that username already exists."),
    #     },
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'required': '',
    #         'placeholder': _("Username"),
    #     })
    # )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
