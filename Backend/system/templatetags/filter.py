from django import template
from utils.session import set_Session_Value
from system.models import StudentProfile

register = template.Library()

@register.simple_tag
def login_fake(school_IDx, request):

    request.session['user'] = {
        "school_ID": school_IDx,                                                 
        'name': StudentProfile.objects.filter(school_ID=school_IDx).values("name").first(),                                   
        "first_name":StudentProfile.objects.filter(school_ID=school_IDx).values("first_name").first(),
        "last_name": StudentProfile.objects.filter(school_ID=school_IDx).values("last_name").first(),                                  
        'teams': StudentProfile.objects.filter(school_ID=school_IDx).values("teams").first(),                                   
        'email': StudentProfile.objects.filter(school_ID=school_IDx).values("email").first(),   
        "klasse": StudentProfile.objects.filter(school_ID=school_IDx).values("klasse").first(),                                                            
        "stufe": StudentProfile.objects.filter(school_ID=school_IDx).values("stufe").first(),                                                             
        'role': StudentProfile.objects.filter(school_ID=school_IDx).values("role").first(),                                                              

    }

    set_Session_Value(request, "logged_in", True)

    return "main:welcome"