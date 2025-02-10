from django.urls import path, include
from . import views

app_name = "run"

urlpatterns = [
    path("login_fake/", views.run_login),
    path("run/", views.none),
    path("lz_register/", views.lz_register, name="lz_register"),
]
