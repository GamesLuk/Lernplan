import requests
from django.conf import settings
from django.shortcuts import redirect, render
from urllib.parse import urlencode
from utils.session import set_Session_Value, get_Session_Value
from system.models import StudentProfile
from utils.system import debug, getSchool_ID
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

    debug(["Token Response:", token_response_data])



    #----------------------------------------------------- Abrufen ------------------------------------------------------#

    # Benutzerinformationen abrufen
    access_token = token_response_data.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(settings.MICROSOFT_USER_INFO_URL, headers=headers)
    user_info = user_info_response.json()

    debug(["User Info Response:", user_info_response.status_code, user_info_response.json()])


    # Benutzer-Teams abfragen
    teams_response = requests.get(f"https://graph.microsoft.com/v1.0/me/joinedTeams", headers=headers)
    teams_info = teams_response.json()


    # Benutzer-Gruppenmitgliedschaften abfragen
    group_memberships_response = requests.get(f"https://graph.microsoft.com/v1.0/me/memberOf", headers=headers)
    group_memberships_info = group_memberships_response.json()


     # Benutzerprofilbild abfragen
    profile_picture_response = requests.get(f"https://graph.microsoft.com/v1.0/me/photo/$value", headers=headers)
    # Benutzerprofilbild prüfen
    if profile_picture_response.status_code == 200:
        profile_picture = profile_picture_response.content
    else:
        profile_picture = None  # Wenn kein Profilbild vorhanden ist, auf None setzen


    # Benutzer- und Organisationsinformationen abfragen
    tenant_id = user_info.get('id')  # ID des Benutzers
    organisation_response = requests.get(f"https://graph.microsoft.com/v1.0/users/{tenant_id}/memberOf", headers=headers)
    organisation_info = organisation_response.json()


    debug(["User Info:", user_info])


    # Encoden der Bilddatei

    # Angenommen, 'image_bytes' ist die bytes-Daten, die du speichern möchtest
    base64_encoded = base64.b64encode(profile_picture).decode('utf-8')



    #--------------------------------------------------- Speicherung -----------------------------------------------------------------#

    allowed_organisations = settings.SCHUL_IDS

    
    # Wenn die User auf Schule geprüft werden und nicht dazugehören, wird der User redirectet und der Login-Vorgang abgebrochen
    if settings.CHECK_SCHUL_IDS == True and not any(org['id'] in allowed_organisations for org in organisation_info.get('value', [])):
        return redirect("main:welcome")
    

    school_ID = getSchool_ID()
    # Speicherung der Daten in der Session
    request.session['user'] = {
        "school_ID": school_ID,                                                         # 10000, 10001, ...
        'name': user_info.get('displayName'),                                   # Voller Name
        "first_name":user_info.get("givenName"),
        "last_name": user_info.get("surname"),
        'profile_picture': base64_encoded,                                     # Profilbild
        'teams': teams_info.get('value', []),                                   # Teams des Benutzers
        'email': user_info.get('mail') or user_info.get('userPrincipalName'),   # Email
        "klasse": 1,                                                            # a,b,c,d,e, ...
        "stufe": 1,                                                             # 5,6,7,8,9, ...
        'role': 1,                                                              # Schüler, Lehrer, Admin, ...

    }

    # Ausgabe der Email bei DEBUG
    debug([request.session.get("user").get("email")])


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
            'profile_picture': base64_encoded,
            'teams': teams_info.get('value', []),
            "email": user_info.get("mail") or user_info.get('userPrincipalName'),
            "klasse": 1,
            "stufe": 1,
            "role": 1,

        }
    )

    # Falls Profil schon existiert, aktualisieren
    if not created:
        StudentProfile.objects.filter(email=user_info.get("mail") or user_info.get('userPrincipalName')).update(

            profile_picture = base64_encoded,          # Anderen Paramater werden sich nie ändern
            teams = teams_info.get('value', []),
            klasse = 1,
            stufe = 1,
            role = 1,

        )

    # DEBUG zur Kontrolle der Antworten von Microsoft
    debug(["Student Profile Created:", created])
    debug(["Teams Response:", teams_info])
    debug(["Group Memberships Response:", group_memberships_info])




    #------------------------------------------------------ Verarbeiten --------------------------------------------------------#

    # Einloggen
    set_Session_Value(request, "logged_in", True)

    
    # Verarbeitung
    requested_url = get_Session_Value(request, settings.REQUESTED_URL_NAME)

    if requested_url != None:
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        return redirect(requested_url)
    return redirect('main:home')

    #-----------------------------------------------------------------------------------------------------------------------------#
    #-----------------------------------------------------------------------------------------------------------------------------#


def logout(request):
    request.session.flush()  # Löscht alle Sitzungsdaten
    return redirect('main:welcome')
