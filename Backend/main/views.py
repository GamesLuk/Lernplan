from django.shortcuts import render, redirect
from django.contrib import admin
from django.http import HttpResponse
from decorators.permissions import login_required, role_required
from utils.session import set_Session_Value, get_Session_Value
from django.conf import settings
from utils.system import getSchool_ID


# Create your views here.

def welcome(request):
    return render(request, "basic/welcome.html")

def main(request):
    host = request.get_host()
    if host.startswith("admin."):
        return redirect("admin:login")
    return redirect("main:welcome")

def home(request):

    set_Session_Value(request, settings.REQUESTED_URL_NAME, "main:home")

    @login_required
    def home(request):
        return render(request, "basic/home.html")
    
    return home(request)

