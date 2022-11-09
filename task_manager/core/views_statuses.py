from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _, pgettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages

from task_manager.core.forms import StatusForm
from task_manager.core.models import Status
from task_manager.core.views import LoginRequired


class StatusesList(LoginRequired, ListView):
    template_name = 'statuses_list.html'
    context_object_name = 'statuses'
    queryset = Status.objects.only('id', 'name', 'created',)


class CreateStatus(SuccessMessageMixin, LoginRequired, CreateView):
    template_name = 'create.html'
    form_class = StatusForm
    success_url = '/statuses/'
    success_message = _("Status successfully created")
    extra_context = {
        'header': pgettext('Create status page header', 'Create status'),
        'button': pgettext('Create status button', 'Create'),
    }


class UpdateStatus(SuccessMessageMixin, LoginRequired, UpdateView):
    template_name = 'create.html'
    form_class = StatusForm
    model = Status
    success_url = '/statuses/'
    success_message = _("Status successfully updated")
    extra_context = {
        'header': pgettext('Update status page header', 'Update status'),
        'button': pgettext('Update status button', 'Update'),
    }


class DeleteStatus(SuccessMessageMixin, LoginRequired, DeleteView):
    template_name = 'delete.html'
    model = Status
    success_url = '/statuses/'
    success_message = _('Status successfully deleted')
    cant_delete_message = _("Can't delete status because it is in use")
    extra_context = {
        'header': pgettext('Delete status page header', 'Delete status'),
        'button': pgettext('Delete status button', 'Yes, delete'),
    }

    def post(self, request, *args, **kwargs):
        status = Status.objects.get(id=kwargs['pk'])
        if status.task_set.all():
            messages.add_message(request,
                                 messages.WARNING,
                                 self.cant_delete_message)
            return redirect('/tasks/')
        else:
            return super().post(self, request, *args, **kwargs)
