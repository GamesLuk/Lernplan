from decorators.permissions import only_localhost, login_required, only_students
from system.models import StudentProfile, AnmeldungProfile
from utils.system import setKlasse_Role, getLernzeit_ID, debug, getAnmeldung_ID
from utils.session import set_Session_Value
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect
import json
from django.utils import timezone
from system.models import LernzeitProfile

def run_login(request):

    login = request.GET.get("login", " ")
    token = request.GET.get("token", " ")

    if token != "fkji4hht4iifgndfkg":
        return HttpResponse(status=204)

    def login_fake(school_IDx, request):

        request.session['user'] = {
            "school_ID": school_IDx,                                                 
            'name': StudentProfile.objects.filter(school_ID=school_IDx).values("name").first()["name"],                                   
            "first_name":StudentProfile.objects.filter(school_ID=school_IDx).values("first_name").first()["first_name"],
            "last_name": StudentProfile.objects.filter(school_ID=school_IDx).values("last_name").first()["last_name"],                                  
            'teams': StudentProfile.objects.filter(school_ID=school_IDx).values("teams").first()["teams"],                                   
            'email': StudentProfile.objects.filter(school_ID=school_IDx).values("email").first()["email"],   
            "klasse": StudentProfile.objects.filter(school_ID=school_IDx).values("klasse").first()["klasse"],                                                            
            "stufe": StudentProfile.objects.filter(school_ID=school_IDx).values("stufe").first()["stufe"],                                                             
            'role': StudentProfile.objects.filter(school_ID=school_IDx).values("role").first()["role"],                                                              


        }

        setKlasse_Role(school_IDx)

        set_Session_Value(request, "logged_in", True)

        debug([f"Logged in a fake user with school_ID: {school_IDx}"])

        return "main:welcome"
    
    login_fake(login, request)

    return HttpResponse(status=204)

def datensatz(request):
    
    with open('C:\\Users\\lukas\\Documents\\Programming_Programs\\Lernplan\\Zusatz\\lernzeiten.json', 'r') as file:
        data = json.load(file)
        for item in data:
            LernzeitProfile.objects.create(
                name=item['name'],
                fach=item['fach'],
                stufen=item['stufen'],
                teacher=item['lehrer'],
                raum=item['raum'],
                tag=item['tag'],
                stunde=item['stunde'],
                type=item['type'],
                plätze=item['platze'],
                lernzeit_ID=getLernzeit_ID(),
                klasse=" ",
                beschreibung=" ",
                activ=True,
            )

    return HttpResponse("Datensatz erfolgreich erstellt", status=200)

def none(request):

    return HttpResponse(status=204)  # Leere Antwort ohne Inhalt

@csrf_protect
@require_POST
@login_required
@only_students

def lz_register(request):

    debug([request.GET, request, request.GET.get("lz_date")])

    referer = request.META.get('HTTP_REFERER')
    allowed_referer = "https://mzb-lev.de/"

    if not (referer and referer.startswith(allowed_referer)):
        return HttpResponse("Ungültiger Zugriff", status=403)

    AnmeldungProfile.objects.create(
        anmeldung_ID=getAnmeldung_ID(),
        school_ID=request.session['user']['school_ID']["school_ID"],
        lernzeit_ID=request.GET.get("lz_ID"),
        date=timezone.now().date(),  # Datum des Tages
        lz_date=request.GET.get("final_date"),
        stunde=request.POST.get("stunde"),
    )

    return redirect("main:lernzeiten") 