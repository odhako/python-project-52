from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect

# Create your views here.
from django.utils.translation import gettext as _, pgettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.statuses.models import Status
from task_manager.views import LoginRequired


class StatusesList(LoginRequired, ListView):
    template_name = 'list_statuses.html'
    model = Status


class CreateStatus(SuccessMessageMixin, LoginRequired, CreateView):
    template_name = 'form_default.html'
    model = Status
    fields = ['name', ]
    success_url = '/statuses/'
    success_message = _("Status successfully created")
    extra_context = {
        'header': pgettext('Create status page header', 'Create status'),
        'button': pgettext('Create status button', 'Create'),
    }


class UpdateStatus(SuccessMessageMixin, LoginRequired, UpdateView):
    template_name = 'form_default.html'
    model = Status
    fields = ['name', ]
    success_url = '/statuses/'
    success_message = _("Status successfully updated")
    extra_context = {
        'header': pgettext('Update status page header', 'Update status'),
        'button': pgettext('Update status button', 'Update'),
    }


class DeleteStatus(SuccessMessageMixin, LoginRequired, DeleteView):
    template_name = 'delete_default.html'
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
                                 messages.ERROR,
                                 self.cant_delete_message)
            return redirect('/tasks/')
        else:
            return super().post(self, request, *args, **kwargs)
