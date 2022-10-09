from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView


class IndexView(TemplateView):
    template_name = 'index.html'


class UsersView(ListView):
    context_object_name = 'users'
    queryset = User.objects.only(
        'username',
        'first_name',
        'last_name',
        'date_joined')
    template_name = 'users.html'
