"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/all/',views.TodoListView.as_view(),name="todo-list"),
    path("todo/add/",views.TodoCreateView.as_view(),name="todo-create"),
    path("todo/<int:pk>/",views.ToDoDetailView.as_view(),name="todo-detail"),
    path("todo/<int:pk>/remove",views.ToDoDeleteView.as_view(),name="todo-delete"),
    path("todo/<int:pk>/change",views.ToDoUpdateView.as_view(),name="todo-update"),
    path('todo/signup/',views.SignupView.as_view(),name="signup"),
    path('todo/signin/',views.SignInView.as_view(),name="signin"),
    path('todo/signout/',views.SignOutView.as_view(),name="signout"),
]
