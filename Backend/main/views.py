from django.shortcuts import render, redirect
from django.contrib import admin
from django.http import HttpResponse
from decorators.permissions import login_required, role_required, not_Student, only_students
from utils.session import set_Session_Value, get_Session_Value, get_User_Value
from django.conf import settings
from utils.system import getSchool_ID, getDay, debug
from system.models import LernzeitProfile
from django.utils import timezone


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
    @only_students
    def home(request):
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        return render(request, "main/dashboard.html")
    
    return home(request)

def lernzeiten(request):

    set_Session_Value(request, settings.REQUESTED_URL_NAME, "main:lernzeiten")


    @login_required
    @only_students
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

    @login_required
    @only_students
    def lernzeiten_info(request):
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        
        id = request.GET.get("lernzeit_ID", " ")

        # Berechnen von Datum

        lz = LernzeitProfile.objects.filter(lernzeit_ID=id)

        date = timezone.now().astimezone(timezone.get_current_timezone())
        day = date.weekday()
        day += 1
        hour = date.hour
        minute = date.minute

        lz_day = lz.values("tag").first()["tag"]
        if lz_day == "Mo":
            lz_day = 1
        if lz_day == "Mi":
            lz_day = 3
        if lz_day == "Do":  
            lz_day = 4

        if day == lz_day:
            if hour <= 8 and minute < 20:
                final_date = date
            else:
                final_date = date + timezone.timedelta(days=7)

        else:
            # So -> Mo: 1 - 7 = -6 + 7 = 1
            if lz_day - day < 0:
                final_date = date + timezone.timedelta(days=lz_day - day + 7)
            # Mo -> Do: 4 - 1 = 3      = 3
            else:
                final_date = date + timezone.timedelta(days=lz_day - day)



        
        vars = {
            "lernzeit": LernzeitProfile.objects.get(lernzeit_ID=id),
            'timestamp': timezone.now().timestamp(),
            "request": request,
            "final_date": final_date.date(),
        }

        return render(request, "main/lernzeiten_info.html", vars)

    return lernzeiten_info(request)

def lehrer_dashboard(request):

    set_Session_Value(request, settings.REQUESTED_URL_NAME, "main:teacher_home")

    @login_required
    @not_Student
    def teacher_dashboard(request):
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        return render(request, "main/teacher_dashboard.html")

    return teacher_dashboard(request)