from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView as BasicLoginView
from django.shortcuts import redirect
from .forms import UserRegistrationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _
from django.utils.translation import pgettext


# Create your views here.
class UsersView(ListView):
    context_object_name = 'users'
    queryset = User.objects.only(
        'username',
        'first_name',
        'last_name',
        'date_joined')
    template_name = 'users.html'


class CreateUserView(SuccessMessageMixin, CreateView):
    template_name = 'create_user.html'
    form_class = UserRegistrationForm
    success_url = '/'
    success_message = _("User successfully registered")
    extra_context = {
        'header': _('Registration'),
        'button': pgettext('sign up button', 'Sign up'),
    }


class UpdateUserView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'create_user.html'
    form_class = UserRegistrationForm
    success_url = '/'
    success_message = _("User successfully updated")
    extra_context = {
        'header': _('Update user'),
        'button': _('Update'),
    }


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'delete_user.html'
    success_url = '/users/'
    success_message = _('User successfully deleted')
    # rus: Пользователь успешно удалён
