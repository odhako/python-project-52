from django.views.generic import TemplateView
from task_manager.users import forms


class IndexView(TemplateView):
    template_name = 'index.html'
