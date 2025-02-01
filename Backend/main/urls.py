from django.urls import include, path
from . import views
from django.views.generic.base import RedirectView

app_name = "main"

urlpatterns = [
    path("home/", views.home, name="home"),
    path("", views.main, name="main"),
    path("welcome/", views.welcome, name="welcome"),
    path("lernzeiten/", views.lernzeiten, name="lernzeiten"),
]
