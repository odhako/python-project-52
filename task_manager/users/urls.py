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

from . import views

urlpatterns = [
    path('users/', views.UsersView.as_view()),
    path('users/create/', views.CreateUserView.as_view()),
    path('users/<int:pk>/update/', views.UpdateUserView.as_view()),
    path('users/<int:pk>/delete/', views.DeleteUserView.as_view()),
    path('login/', views.LoginUserView.as_view()),
    path('logout/', views.LogoutUserView.as_view()),
]
