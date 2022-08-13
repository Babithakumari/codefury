from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path("create", views.create, name="create"),
    path("edit/<int:s_id>",views.edit, name="edit"),
    path("delete/<int:s_id>", views.delete,name="delete"),

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
