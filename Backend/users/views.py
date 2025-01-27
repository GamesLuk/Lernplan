from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

def redirect_to_microsoft_login(request):
    return redirect(reverse("socialaccount_login", kwargs={"provider":"microsoft"}))