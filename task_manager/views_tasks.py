from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _, pgettext
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, TemplateView
from django_filters.views import FilterView

from .forms import TaskForm
from .models import Task
from .views import LoginRequired
from .filters import TaskFilter


# class TasksList(LoginRequired, TemplateView):
#     template_name = 'list_tasks.html'
#
#     def get(self, request, *args, **kwargs):
#         task_filter = TaskFilter(request.GET or None)
#         q = Task.objects.only('id', 'name', 'status', 'author',
#                                     'executor', 'created')
#
#         # Filter:
#         if request.GET:
#             if 'status' in request.GET and request.GET['status'] != '':
#                 q = q.filter(status=request.GET['status'])
#             if 'executor' in request.GET and request.GET['executor'] != '':
#                 q = q.filter(executor=request.GET['executor'])
#             if 'label' in request.GET and request.GET['label'] != '':
#                 q = q.filter(labels=request.GET['label'])
#             if 'self_tasks' in request.GET and request.GET['self_tasks']:
#                 q = q.filter(author=request.user.id)
#
#         context = self.get_context_data()
#         context['filter'] = task_filter
#         context['tasks'] = q
#         return self.render_to_response(context)


class CreateTask(SuccessMessageMixin, LoginRequired, CreateView):
    template_name = 'form_default.html'
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
    template_name = 'form_default.html'
    form_class = TaskForm
    model = Task
    success_url = '/tasks/'
    success_message = _("Task successfully updated")
    extra_context = {
        'header': pgettext('Update task page header', 'Update task'),
        'button': pgettext('Update task button', 'Update'),
    }


class DeleteTask(SuccessMessageMixin, LoginRequired, DeleteView):
    template_name = 'delete_default.html'
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


class TasksList(LoginRequired, FilterView):
    template_name = 'list_tasks.html'
    queryset = Task.objects.all()
    context_object_name = 'tasks'
    filterset_class = TaskFilter
