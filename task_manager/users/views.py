from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, CreateView
from django.contrib.auth.views import LoginView as BasicLoginView
from django.shortcuts import redirect
from .forms import UserRegistrationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _


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
