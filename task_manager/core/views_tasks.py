from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _, pgettext
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic import DetailView

from task_manager.core.forms import TaskForm
from task_manager.core.models import Task
from task_manager.core.views import LoginRequired


class TasksList(LoginRequired, ListView):
    template_name = 'tasks_list.html'
    context_object_name = 'tasks'
    queryset = Task.objects.only('id', 'name', 'status', 'author',
                                 'executor', 'created')


class CreateTask(SuccessMessageMixin, LoginRequired, CreateView):
    template_name = 'create.html'
    form_class = TaskForm
    success_url = '/tasks/'
    success_message = _("Task successfully created")
    # rus: Задача успешно создана
    extra_context = {
        'header': pgettext('Create task page header', 'Create task'),
        # rus: Создать задачу
        'button': pgettext('Create task button', 'Create'),
        # rus: Создать
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
    # rus: Задача успешно изменена
    extra_context = {
        'header': pgettext('Update task page header', 'Update task'),
        # rus: Изменение задачи
        'button': pgettext('Update task button', 'Update'),
        # rus: Изменить
    }


class DeleteTask(SuccessMessageMixin, LoginRequired, DeleteView):
    template_name = 'delete.html'
    model = Task
    success_url = '/tasks/'
    success_message = _('Task successfully deleted')
    permission_denied_message = _("Only author of the task can delete it")
    # rus: Задача успешно удалена
    extra_context = {
        'header': pgettext('Delete task page header', 'Delete task'),
        # rus: Удаление задачи
        'button': pgettext('Delete task button', 'Yes, delete'),
        # rus: Да, удалить
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
