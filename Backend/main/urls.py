from django.urls import include, path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path("home/", views.home),
    path("", RedirectView.as_view(url='/home/')),
]
