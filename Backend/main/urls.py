from django.urls import include, path
from . import views
from django.views.generic.base import RedirectView

app_name = "main"

urlpatterns = [
    path("home/", views.home, name="home"),
    path("home/inside/", views.inside, name="inside"),
    path("", views.main, name="main"),
]
