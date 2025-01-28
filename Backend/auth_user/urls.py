from django.urls import path, include
from . import views

app_name = "auth"

urlpatterns = [
    path("login/", views.microsoft_login, name="login"),
    path("callback/", views.microsoft_callback, name="callback"),
]
