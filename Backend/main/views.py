from django.shortcuts import render, redirect
from django.contrib import admin
from django.http import HttpResponse
import requests
from auth_user.decorators import login_required, role_required

# Create your views here.

def home(request):
    return render(request, "home.html")

def main(request):
    host = request.get_host()
    if host.startswith("admin."):
        return redirect("admin:login")
    return redirect("/home/")

def inside(request):
    request.session["requested_url"] = request.get_host()
    return render(request, "inside.html")