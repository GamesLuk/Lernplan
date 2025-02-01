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
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        return render(request, "basic/home.html")
    
    return home(request)

def lernzeiten(request):

    set_Session_Value(request, settings.REQUESTED_URL_NAME, "main:lernzeiten")

    @login_required
    def lernzeiten(request):
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)

        vars = {
            "lernzeiten": [
                {
                    "name": "Mathe",
                    "fach": "Mathe",
                    "datum": "2021-08-24",
                    "lehrer": "Herr Müller",
                    "stunde": "3",
                    "raum": "A-123",
                    "link": "https://www.google.com",
                },
                {
                    "name": "Englisch",
                    "fach": "Englisch",
                    "datum": "2021-08-25",
                    "lehrer": "Frau Schmidt",
                    "stunde": "2",
                    "raum": "B-234",
                    "link": "https://www.bing.com",
                },
                {
                    "name": "Biologie",
                    "fach": "Biologie",
                    "datum": "2021-08-26",
                    "lehrer": "Herr Fischer",
                    "stunde": "4",
                    "raum": "C-345",
                    "link": "https://www.yahoo.com",
                },
                {
                    "name": "Chemie",
                    "fach": "Chemie",
                    "datum": "2021-08-27",
                    "lehrer": "Frau Weber",
                    "stunde": "1",
                    "raum": "D-456",
                    "link": "https://www.duckduckgo.com",
                },
                {
                    "name": "Physik",
                    "fach": "Physik",
                    "datum": "2021-08-28",
                    "lehrer": "Herr Becker",
                    "stunde": "5",
                    "raum": "E-567",
                    "link": "https://www.ask.com",
                },
            ],
        }

        return render(request, "basic/lernzeiten.html", vars)
    
    return lernzeiten(request)