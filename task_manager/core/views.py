from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView
from .models import Status
from .forms import StatusForm
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import pgettext
from django.utils.translation import gettext as _


class StatusesList(ListView):
    template_name = 'statuses_list.html'
    context_object_name = 'statuses'
    queryset = Status.objects.only('id', 'name', 'created',)


class CreateStatus(SuccessMessageMixin, CreateView):
    template_name = 'create_user.html'
    form_class = StatusForm
    success_url = '/statuses/'
    success_message = _("Status successfully created")
    # rus: Статус успешно создан
    extra_context = {
        'header': pgettext('Create status page header', 'Create status'),
        # rus: Создать статус
        'button': pgettext('Create status button', 'Create'),
        # rus: Создать
    }


class UpdateStatus(SuccessMessageMixin, UpdateView):
    template_name = 'create_user.html'
    form_class = StatusForm
    model = Status
    success_url = '/statuses/'
    success_message = _("Status successfully updated")
    # rus: Статус успешно изменён
    extra_context = {
        'header': pgettext('Update status page header', 'Update status'),
        # rus: Изменение статуса
        'button': pgettext('Update status button', 'Update'),
        # rus: Изменить
    }


class DeleteStatus(SuccessMessageMixin, DeleteView):
    template_name = 'delete.html'
    model = Status
    success_url = '/statuses/'
    success_message = _('Status successfully deleted')
    # rus: Статус успешно удалён
    extra_context = {
        'header': pgettext('Delete status page header', 'Delete status'),
        # rus: Удаление статуса
        'button': pgettext('Delete status button', 'Yes, delete'),
        # rus: Да, удалить
    }
