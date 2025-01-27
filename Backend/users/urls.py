from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.redirect_to_microsoft_login, name="redirect_to_microsoft")
]


