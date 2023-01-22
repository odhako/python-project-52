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
from django.contrib import admin
from django.urls import path

import task_manager.statuses.views
import task_manager.users.views
from task_manager import views
from task_manager import views_tasks, views_labels

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view()),
    path('users/', task_manager.users.views.UsersView.as_view()),
    path('users/create/', task_manager.users.views.CreateUserView.as_view()),
    path('users/<int:pk>/update/', task_manager.users.views.UpdateUserView.as_view()),
    path('users/<int:pk>/delete/', task_manager.users.views.DeleteUserView.as_view()),
    path('login/', task_manager.users.views.LoginUserView.as_view()),
    path('logout/', task_manager.users.views.LogoutUserView.as_view()),
    path('statuses/', task_manager.statuses.views.StatusesList.as_view()),
    path('statuses/create/', task_manager.statuses.views.CreateStatus.as_view()),
    path('statuses/<int:pk>/update/', task_manager.statuses.views.UpdateStatus.as_view()),
    path('statuses/<int:pk>/delete/', task_manager.statuses.views.DeleteStatus.as_view()),
    path('tasks/', views_tasks.TasksList.as_view()),
    path('tasks/create/', views_tasks.CreateTask.as_view()),
    path('tasks/<int:pk>/update/', views_tasks.UpdateTask.as_view()),
    path('tasks/<int:pk>/delete/', views_tasks.DeleteTask.as_view()),
    path('tasks/<int:pk>/', views_tasks.TaskView.as_view()),
    path('labels/', views_labels.LabelsList.as_view()),
    path('labels/create/', views_labels.CreateLabel.as_view()),
    path('labels/<int:pk>/update/', views_labels.UpdateLabel.as_view()),
    path('labels/<int:pk>/delete/', views_labels.DeleteLabel.as_view()),
]
