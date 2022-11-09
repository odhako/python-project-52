from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext as _, pgettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages

from task_manager.core.forms import LabelForm
from task_manager.core.models import Label
from task_manager.core.views import LoginRequired


class LabelsList(LoginRequired, ListView):
    template_name = 'labels_list.html'
    context_object_name = 'labels'
    queryset = Label.objects.only('id', 'name', 'created')


class CreateLabel(SuccessMessageMixin, LoginRequired, CreateView):
    template_name = 'create.html'
    form_class = LabelForm
    success_url = '/labels/'
    success_message = _('Label successfully created')
    extra_context = {
        'header': pgettext('Create label page header', 'Create label'),
        'button': pgettext('Create label button', 'Create'),
    }


class UpdateLabel(SuccessMessageMixin, LoginRequired, UpdateView):
    template_name = 'create.html'
    form_class = LabelForm
    model = Label
    success_url = '/labels/'
    success_message = _("Label successfully updated")
    extra_context = {
        'header': pgettext('Update label page header', 'Update label'),
        'button': pgettext('Update label button', 'Update'),
    }


class DeleteLabel(SuccessMessageMixin, LoginRequired, DeleteView):
    template_name = 'delete.html'
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
