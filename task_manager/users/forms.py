from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from task_manager.users.models import User


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
