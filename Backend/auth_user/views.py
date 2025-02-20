from django.forms import CharField
import requests
from django.conf import settings
from django.shortcuts import redirect, render
from urllib.parse import urlencode
from utils.session import set_Session_Value, get_Session_Value
from system.models import StudentProfile, system
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

    if profile_picture_base64 == "eyJlcnJvciI6eyJjb2RlIjoiSW1hZ2VOb3RGb3VuZCIsIm1lc3NhZ2UiOiJFeGNlcHRpb24gb2YgdHlwZSAnTWljcm9zb2Z0LkZhc3QuUHJvZmlsZS5Db3JlLkV4Y2VwdGlvbi5JbWFnZU5vdEZvdW5kRXhjZXB0aW9uJyB3YXMgdGhyb3duLiIsImlubmVyRXJyb3IiOnsiZGF0ZSI6IjIwMjUtMDItMjBUMDg6NDI6NDQiLCJyZXF1ZXN0LWlkIjoiMWYzOTNiOGEtY2E3Mi00ZWFiLTk4MzItZGM0MjZhODVkNjhkIiwiY2xpZW50LXJlcXVlc3QtaWQiOiIxZjM5M2I4YS1jYTcyLTRlYWItOTgzMi1kYzQyNmE4NWQ2OGQifX19":
        profile_picture_base64 = "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"


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
    
    url="main:dashboard"

    if request.session.get("user").get("role") == "2":
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

