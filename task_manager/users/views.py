from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _, pgettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.users.forms import UserForm, UserLoginForm


class BasicPermissionsMixin(LoginRequiredMixin):
    login_url = '/login/'
    permission_denied_message = _("You don't have rights to edit other users")
    login_required_message = _("You are not authorised! Please log in.")

    def get(self, request, *args, **kwargs):
        # print('Current user id:', request.user.id)
        # print('Request pk:', self.kwargs['pk'])
        if request.user.id != self.kwargs['pk']:
            messages.add_message(request,
                                 messages.ERROR,
                                 self.permission_denied_message)
            return redirect('/users/')
        elif request.user.id == self.kwargs['pk']:
            return super().get(self, request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.ERROR,
                                 self.login_required_message)
            return self.handle_no_permission()
        else:
            return super().dispatch(request, *args, **kwargs)


class UsersView(ListView):
    context_object_name = 'users'
    queryset = User.objects.only(
        'username',
        'first_name',
        'last_name',
        'date_joined')
    template_name = 'list_users.html'


class CreateUserView(SuccessMessageMixin, CreateView):
    template_name = 'form_default.html'
    form_class = UserForm
    success_url = '/login/'
    success_message = _("User successfully registered")
    extra_context = {
        'header': _('Registration'),
        'button': pgettext('sign up button', 'Sign up'),
    }


class UpdateUserView(BasicPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'form_default.html'
    form_class = UserForm
    success_url = '/users/'
    success_message = _("User successfully updated")
    extra_context = {
        'header': _('Update user'),
        'button': _('Update'),
    }


class DeleteUserView(BasicPermissionsMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'delete_user.html'
    success_url = '/users/'
    success_message = _('User successfully deleted')
    cant_delete_message = _("Can't delete user because it is in use")

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        if user.task_author.all() or user.task_executor.all():
            messages.add_message(request,
                                 messages.ERROR,
                                 self.cant_delete_message)
            return redirect('/users/')
        else:
            return super().post(self, request, *args, **kwargs)


class LoginUserView(SuccessMessageMixin, LoginView):
    template_name = 'form_default.html'
    form_class = UserLoginForm
    next_page = '/'
    redirect_authenticated_user = False
    success_message = _('You are logged in')
    extra_context = {
        'header': pgettext('Login page header', 'Log in'),
        'button': pgettext('Login page button', 'Log in'),
    }


class LogoutUserView(LogoutView):
    next_page = '/'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, _('You are logged out'))
        return response
