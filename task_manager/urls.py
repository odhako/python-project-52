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
from task_manager import views
from task_manager import views_tasks, views_users, views_labels
from task_manager.statuses import views as views_statuses

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view()),
    path('users/', views_users.UsersView.as_view()),
    path('users/create/', views_users.CreateUserView.as_view()),
    path('users/<int:pk>/update/', views_users.UpdateUserView.as_view()),
    path('users/<int:pk>/delete/', views_users.DeleteUserView.as_view()),
    path('login/', views_users.LoginUserView.as_view()),
    path('logout/', views_users.LogoutUserView.as_view()),
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
