"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

import task_manager.core.views_statuses
import task_manager.core.views_tasks

urlpatterns = [
    path('statuses/', task_manager.core.views_statuses.StatusesList.as_view()),
    path('statuses/create/', task_manager.core.views_statuses.CreateStatus.as_view()),
    path('statuses/<int:pk>/update/', task_manager.core.views_statuses.UpdateStatus.as_view()),
    path('statuses/<int:pk>/delete/', task_manager.core.views_statuses.DeleteStatus.as_view()),
    path('tasks/', task_manager.core.views_tasks.TasksList.as_view()),
    path('tasks/create/', task_manager.core.views_tasks.CreateTask.as_view()),
    path('tasks/<int:pk>/update/', task_manager.core.views_tasks.UpdateTask.as_view()),
    path('tasks/<int:pk>/delete/', task_manager.core.views_tasks.DeleteTask.as_view()),
    path('tasks/<int:pk>/', task_manager.core.views_tasks.TaskView.as_view()),
]
