from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from .models import Status
from .forms import StatusForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import pgettext as _


class StatusesList(ListView):
    template_name = 'statuses_list.html'
    context_object_name = 'statuses'
    queryset = Status.objects.only('id', 'name', 'created',)


class CreateStatus(SuccessMessageMixin, CreateView):
    template_name = 'create_user.html'
    form_class = StatusForm
    success_url = '/statuses/'
    success_message = _('Success message', "Status successfully created")
    # rus: Статус успешно создан
    extra_context = {
        'header': _('Create status page header', 'Create status'),
        # rus: Создать статус
        'button': _('Create status button', 'Create'),
        # rus: Создать
    }


class UpdateStatus(SuccessMessageMixin, UpdateView):
    template_name = 'create_user.html'
    form_class = StatusForm
    model = Status
    success_url = '/statuses/'
    success_message = _('Success message', "Status successfully updated")
    # rus: Статус успешно изменён
    extra_context = {
        'header': _('Update status page header', 'Update status'),
        # rus: Изменение статуса
        'button': _('Update status button', 'Update'),
        # rus: Изменить
    }


class DeleteStatus(SuccessMessageMixin, DeleteView):
    template_name = 'delete.html'
    model = Status
    success_url = '/statuses/'
    success_message = _('Success message', 'Status successfully deleted')
    # rus: Статус успешно удалён
    extra_context = {
        'header': _('Delete status page header', 'Delete status'),
        # rus: Удаление статуса
        'button': _('Delete status button', 'Yes, delete'),
        # rus: Да, удалить
    }
