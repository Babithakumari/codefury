from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path("create", views.create, name="create"),
    path("edit/<int:s_id>",views.edit, name="edit"),
    path("delete/<int:s_id>", views.delete,name="delete"),
    path("search", views.search, name="search"),
    path("favourites", views.favourites, name="favourites"),
    path("startup/<int:s_id>", views.startup, name="startup"),
    path("investments", views.investments, name="investments"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("order_payment/", views.order_payment, name="order_payment"),
    path("callback/", views.callback, name="callback"),
    path('invest/', views.invest, name="invest"),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]
