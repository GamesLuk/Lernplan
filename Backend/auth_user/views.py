import requests
from django.conf import settings
from django.shortcuts import redirect, render
from urllib.parse import urlencode
from utils.session import set_Session_Value, get_Session_Value
from system_control.models import StudentProfile


# Create your views here.

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






    #------------------------------------ Abrufen ------------------------------------------------------#

    # Benutzerinformationen abrufen
    access_token = token_response_data.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(settings.MICROSOFT_USER_INFO_URL, headers=headers)
    user_info = user_info_response.json()

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




    #----------------------------------------- Speicherung -----------------------------------------------------------------------#

    allowed_organisations = settings.SCHUL_IDS

    if settings.CHECK_SCHUL_IDS == True and not any(org['id'] in allowed_organisations for org in organisation_info.get('value', [])):
        return redirect("main:welcome")
    
    request.session['user'] = {
        'name': user_info.get('displayName'),
        'email': user_info.get('mail') or user_info.get('userPrincipalName'),
        'role': None,
        'teams': teams_info.get('value', []),  # Teams des Benutzers
        'profile_picture': profile_picture,  # Profilbild
    }

    print(request.session.get("user").get("email"))

    student_profile, created = StudentProfile.objects.update_or_create(
        email=user_info.get('mail') or user_info.get('userPrincipalName'),
        defaults={
            "school_ID": 1,
            'name': user_info.get('displayName') or 1,
            'profile_picture': profile_picture or 1,
            'teams': teams_info.get('value', []),
            "email": user_info.get("mail") or user_info.get('userPrincipalName') or 1,
            "klasse": 1,
            "stufe": 1,
        }
    )

    # Einloggen
    set_Session_Value(request, "logged_in", True)

    
    # Verarbeitung
    requested_url = get_Session_Value(request, settings.REQUESTED_URL_NAME)

    if requested_url != None:
        set_Session_Value(request, settings.REQUESTED_URL_NAME, None)
        return redirect(requested_url)
    return redirect('main:home')



def logout(request):
    request.session.flush()  # Löscht alle Sitzungsdaten
    return redirect('main:welcome')
