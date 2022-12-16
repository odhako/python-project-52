from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _, pgettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.labels.models import Label
from task_manager.views import LoginRequired


class LabelsList(LoginRequired, ListView):
    template_name = 'list_labels.html'
    model = Label


class CreateLabel(SuccessMessageMixin, LoginRequired, CreateView):
    template_name = 'form_default.html'
    model = Label
    fields = ['name', ]
    success_url = '/labels/'
    success_message = _('Label successfully created')
    extra_context = {
        'header': pgettext('Create label page header', 'Create label'),
        'button': pgettext('Create label button', 'Create'),
    }


class UpdateLabel(SuccessMessageMixin, LoginRequired, UpdateView):
    template_name = 'form_default.html'
    model = Label
    fields = ['name', ]
    success_url = '/labels/'
    success_message = _("Label successfully updated")
    extra_context = {
        'header': pgettext('Update label page header', 'Update label'),
        'button': pgettext('Update label button', 'Update'),
    }


class DeleteLabel(SuccessMessageMixin, LoginRequired, DeleteView):
    template_name = 'delete_default.html'
    model = Label
    success_url = '/labels/'
    success_message = _('Label successfully deleted')
    cant_delete_message = _("Can't delete label because it is in use")
    extra_context = {
        'header': pgettext('Delete label page header', 'Delete label'),
        'button': pgettext('Delete label button', 'Yes, delete'),
    }

    def post(self, request, *args, **kwargs):
        label = Label.objects.get(id=kwargs['pk'])
        if label.task_set.all():
            messages.add_message(request,
                                 messages.WARNING,
                                 self.cant_delete_message)
            return redirect('/labels/')
        else:
            return super().post(self, request, *args, **kwargs)
