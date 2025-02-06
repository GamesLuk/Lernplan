from django.shortcuts import render, redirect
from django.contrib import admin
from django.http import HttpResponse
from decorators.permissions import login_required, role_required
from utils.session import set_Session_Value, get_Session_Value, get_User_Value
from django.conf import settings
from utils.system import getSchool_ID, getDay, debug
from system.models import LernzeitProfile


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
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        return render(request, "basic/home.html")
    
    return home(request)

def lernzeiten(request):

    set_Session_Value(request, settings.REQUESTED_URL_NAME, "main:lernzeiten")

    @login_required
    def lernzeiten(request):
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)

        klasse = str(get_User_Value(request, "stufe")) + get_User_Value(request, "klasse")
        stufe = get_User_Value(request, "stufe")


        if not stufe >= 11:
            lernzeiten = LernzeitProfile.objects.filter(stufen__contains=stufe).all()
        
        def nextMonday():
            from datetime import datetime, timedelta
            today = datetime.today()
            days_ahead = 0 - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days_ahead)
        
        def nextThursday():
            from datetime import datetime, timedelta
            today = datetime.today()
            days_ahead = 3 - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days_ahead)
        
        debug([nextMonday(), nextThursday()])

        vars = {
            "klasse":klasse,
            "lernzeiten":lernzeiten,
        }

        return render(request, "main/lernzeiten.html", vars)
    
    return lernzeiten(request)


def lernzeiten_info(request):

    set_Session_Value(request, settings.REQUESTED_URL_NAME, "main:lernzeiten_info")

    def lernzeiten_info(request):
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        
        id = request.GET.get("id", " ")

        return render(request, "main/lernzeiten_info.html")

    return lernzeiten_info(request)