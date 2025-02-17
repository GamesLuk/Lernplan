from django.forms import CharField
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from urllib.parse import urlencode
from utils.session import set_Session_Value, get_Session_Value
from system.models import StudentProfile
from utils.system import debug, getSchool_ID, setKlasse_Role
from django.http import HttpResponse
from django.db.models.functions import Cast
from decorators.permissions import login_required, role_required
from django.core.files.base import ContentFile
import base64


def microsoft_login(request):
    params = {
        'client_id': settings.MICROSOFT_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': settings.MICROSOFT_REDIRECT_URI,
        'response_mode': 'query',
        'scope': ' '.join(settings.SCOPES),  # Nutze die Scopes aus den Settings
    }
    url = f"{settings.MICROSOFT_AUTHORIZATION_URL}?{urlencode(params)}"
    return redirect(url)


#-----------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------------------------------------------------#

def microsoft_callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect("main:home")

    # Zugriffstoken abrufen
    token_data = {
        'client_id': settings.MICROSOFT_CLIENT_ID,
        'client_secret': settings.MICROSOFT_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.MICROSOFT_REDIRECT_URI,
    }
    token_response = requests.post(settings.MICROSOFT_TOKEN_URL, data=token_data)
    token_response_data = token_response.json()

    #debug(["Token Response:", token_response_data])



    #----------------------------------------------------- Abrufen ------------------------------------------------------#

    # Benutzerinformationen abrufen
    access_token = token_response_data.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(settings.MICROSOFT_USER_INFO_URL, headers=headers)
    user_info = user_info_response.json()

    #debug(["User Info Response:", user_info_response.status_code, user_info_response.json()])


    # Benutzer-Teams abfragen
    teams_response = requests.get(f"https://graph.microsoft.com/v1.0/me/joinedTeams", headers=headers)
    teams_info = teams_response.json()


    # Benutzer-Gruppenmitgliedschaften abfragen
    group_memberships_response = requests.get(f"https://graph.microsoft.com/v1.0/me/memberOf", headers=headers)
    group_memberships_info = group_memberships_response.json()


    # Benutzer- und Organisationsinformationen abfragen
    teams = teams_info.get("value", [])
    tenant_id = teams[0]["tenantId"] if teams else None
    organisation_response = requests.get(f"https://graph.microsoft.com/v1.0/users/{tenant_id}/memberOf", headers=headers)
    organisation_info = organisation_response.json()


    #debug(["User Info:", user_info])

    # Fetch profile picture URL
    profile_picture_url = f"https://graph.microsoft.com/v1.0/me/photo/$value"

    # Fetch profile picture
    profile_picture_response = requests.get(profile_picture_url, headers=headers)
    profile_picture_content = profile_picture_response.content
    profile_picture_base64 = base64.b64encode(profile_picture_content).decode('utf-8')


    #--------------------------------------------------- Speicherung -----------------------------------------------------------------#

    
    # Wenn die User auf Schule geprüft werden und nicht dazugehören, wird der User redirectet und der Login-Vorgang abgebrochen
    if settings.CHECK_SCHUL_IDS == True and not tenant_id == settings.SCHUL_IDS:
        return redirect("main:welcome")
    
    school_ID = 0

    if not StudentProfile.objects.filter(email=user_info.get("mail")):
        school_ID = getSchool_ID()
    

    # Ausgabe der Email bei DEBUG
    #debug([request.session.get("user").get("email")])


    # Speicherung der Daten in der Datenbank
    # Prüfen, ob Profil schon besteht
    student_profile, created = StudentProfile.objects.get_or_create(

        email=user_info.get("mail") or user_info.get('userPrincipalName'),          # Prüfen über Email
        defaults={
                                                                                    # Wenn nicht, dann Profil erstellen
            "school_ID": school_ID,
            'name': user_info.get('displayName'),
            "first_name":user_info.get("givenName"),
            "last_name": user_info.get("surname"),
            'teams': teams_info.get('value', []),
            "email": user_info.get("mail") or user_info.get('userPrincipalName'),
            "klasse": 0,
            "stufe": 0,
            "role": 1,
            "profile_picture": profile_picture_base64,

        }
    )

    # Falls Profil schon existiert, aktualisieren
    if not created:
        StudentProfile.objects.filter(email=user_info.get("mail") or user_info.get('userPrincipalName')).update(

            teams = teams_info.get('value', []),
            profile_picture=profile_picture_base64,

        )
        if settings.DEBUG:
            setKlasse_Role(StudentProfile.objects.filter(email=user_info.get("mail")).values("school_ID").first()["school_ID"])
    else:
        setKlasse_Role(StudentProfile.objects.filter(email=user_info.get("mail")).values("school_ID").first()["school_ID"])



    # Speicherung der Daten in der Session
    request.session['user'] = {
        "school_ID": StudentProfile.objects.filter(email=user_info.get("mail")).values("school_ID").first()["school_ID"],                                                 # 10000, 10001, ...
        'name': user_info.get('displayName'),                                   # Voller Name
        "first_name":user_info.get("givenName"),
        "last_name": user_info.get("surname"),                                  
        'teams': teams_info.get('value', []),                                   # Teams des Benutzers
        'email': user_info.get('mail') or user_info.get('userPrincipalName'),   # Email
        "klasse": StudentProfile.objects.filter(email=user_info.get("mail")).values("klasse").first(),                                                            # a,b,c,d,e, ...
        "stufe": StudentProfile.objects.filter(email=user_info.get("mail")).values("stufe").first(),                                                             # 5,6,7,8,9, ...
        'role': StudentProfile.objects.filter(email=user_info.get("mail")).values("role").first(),                                                              # Schüler, Lehrer, Admin, ...
        "profile_picture": profile_picture_base64,

    }

    # DEBUG zur Kontrolle der Antworten von Microsoft
    #debug(["Student Profile Created:", created])
    #debug(["Teams Response:", teams_info])
    #debug(["Group Memberships Response:", group_memberships_info])






    #------------------------------------------------------ Verarbeiten --------------------------------------------------------#

    # Einloggen
    set_Session_Value(request, "logged_in", True)
    
    url="main:home"

    if request.session.get("user").get("role") == 3:
        url = "main:lehrer_dashboard"


    # Verarbeitung
    requested_url = get_Session_Value(request, settings.REQUESTED_URL_NAME)

    if requested_url != None:
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        return redirect(requested_url)
    return redirect(url)

    #-----------------------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------#


def logout(request):
    request.session.flush()  # Löscht alle Sitzungsdaten
    return redirect('main:welcome')




def fake_login(request):

    set_Session_Value(request, settings.REQUESTED_URL_NAME, "auth:fake_login")
    
    @login_required
    def fake_login(request):
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        vars = {
            "fakes": get_Fakes(),
            "request": request,
            "token": settings.TOKEN
        }
        return render(request, "basic/fake_login.html", vars)
    
    return fake_login(request)


def get_Fakes():
    return list(StudentProfile.objects.filter(school_ID__startswith="9").values_list("school_ID", flat=True))


@login_required
def profile_view(request):
    user_profile = StudentProfile.objects.get(email=request.user.email)
    return render(request, 'main/profile.html', {'user': user_profile})

