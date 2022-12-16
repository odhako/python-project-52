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
from django.urls import path, include

from task_manager import views

from .users import urls as users
from .statuses import urls as statuses
from .tasks import urls as tasks
from .labels import urls as labels


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view()),
    path('', include(users)),
    path('statuses/', include(statuses)),
    path('tasks/', include(tasks)),
    path('labels/', include(labels)),
]
