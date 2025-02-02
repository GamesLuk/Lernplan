from django.urls import path, include
from . import views

urlpatterns = [
    path("login_fake/", views.run_login),
    path("run/", views.none),
]
