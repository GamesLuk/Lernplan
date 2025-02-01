from decorators.permissions import only_localhost
from system.models import StudentProfile
from utils.system import setKlasse_Role
from utils.session import set_Session_Value
from django.http import HttpResponse

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
