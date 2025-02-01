from django import template
from utils.session import set_Session_Value
from system.models import StudentProfile
from utils.system import setKlasse_Role

register = template.Library()

@register.simple_tag
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