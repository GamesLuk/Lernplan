from django.urls import include, path
from . import views
from django.views.generic.base import RedirectView

app_name = "main"

urlpatterns = [
    path("home/", views.home, name="home"),
    path("dashboard/", views.home, name="dashboard"),
    path("", views.main, name="main"),
    path("welcome/", views.welcome, name="welcome"),
    path("lernzeiten/", views.lernzeiten, name="lernzeiten"),
    path("lernzeiten/info/", views.lernzeiten_info, name="lernzeiten_info"),
    path("lehrer/", views.lehrer, name="lehrer"),
    path("lehrer/dashboard/", views.lehrer_dashboard, name="lehrer_dashboard"),
    path("lernzeiten/kalender/", views.lernzeit_calendar, name="termine"),
    path("profile/", views.profile_view, name="profile"),
]
