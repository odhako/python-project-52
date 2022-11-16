from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _, pgettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView

from task_manager.core.forms import TaskForm, TaskFilter
from task_manager.core.models import Task
from task_manager.core.views import LoginRequired


class TasksList(LoginRequired, TemplateView):
    template_name = 'tasks_list.html'

    def get(self, request, *args, **kwargs):
        task_filter = TaskFilter(request.GET or None)
        q = Task.objects.only('id', 'name', 'status', 'author',
                                    'executor', 'created')

        # Filter:
        if request.GET:
            if request.GET['status']:
                q = q.filter(status=request.GET['status'])
            if request.GET['executor']:
                q = q.filter(executor=request.GET['executor'])
            if request.GET['label']:
                q = q.filter(labels=request.GET['label'])
            if 'self_tasks' in request.GET:
                q = q.filter(author=request.user.id)

        context = self.get_context_data()
        context['task_filter'] = task_filter
        context['tasks'] = q
        return self.render_to_response(context)


class CreateTask(SuccessMessageMixin, LoginRequired, CreateView):
    template_name = 'create.html'
    form_class = TaskForm
    success_url = '/tasks/'
    success_message = _("Task successfully created")
    extra_context = {
        'header': pgettext('Create task page header', 'Create task'),
        'button': pgettext('Create task button', 'Create'),
    }

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super().form_valid(form)


class UpdateTask(SuccessMessageMixin, LoginRequired, UpdateView):
    template_name = 'create.html'
    form_class = TaskForm
    model = Task
    success_url = '/tasks/'
    success_message = _("Task successfully updated")
    extra_context = {
        'header': pgettext('Update task page header', 'Update task'),
        'button': pgettext('Update task button', 'Update'),
    }


class DeleteTask(SuccessMessageMixin, LoginRequired, DeleteView):
    template_name = 'delete.html'
    model = Task
    success_url = '/tasks/'
    success_message = _('Task successfully deleted')
    permission_denied_message = _("Only author of the task can delete it")
    extra_context = {
        'header': pgettext('Delete task page header', 'Delete task'),
        'button': pgettext('Delete task button', 'Yes, delete'),
    }

    def get(self, request, *args, **kwargs):
        task_to_delete = Task.objects.get(id=self.kwargs['pk'])
        if request.user.id != task_to_delete.author.id:
            messages.add_message(request,
                                 messages.WARNING,
                                 self.permission_denied_message)
            return redirect('/tasks/')
        else:
            return super().get(self, request, *args, **kwargs)


class TaskView(DetailView):
    template_name = 'task.html'
    context_object_name = 'task'

    def get_object(self, queryset=None):
        return Task.objects.get(id=self.kwargs['pk'])
