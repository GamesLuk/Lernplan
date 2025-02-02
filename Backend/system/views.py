from decorators.permissions import only_localhost
from system.models import StudentProfile
from utils.system import setKlasse_Role, getLernzeit_ID
from utils.session import set_Session_Value
from django.http import HttpResponse
import json
from system.models import LernzeitProfile

def run_login(request):

    login = request.GET.get("login", " ")
    token = request.GET.get("token", " ")

    if token != "fkji4hht4iifgndfkg":
        return

    def login_fake(school_IDx, request):

        setKlasse_Role(school_IDx)

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

        set_Session_Value(request, "logged_in", True)

        return "main:welcome"
    
    login_fake(login, request)

    return HttpResponse(status=204)  # Leere Antwort ohne Inhalt

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