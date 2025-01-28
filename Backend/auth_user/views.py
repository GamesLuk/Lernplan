import requests
from django.conf import settings
from django.shortcuts import redirect, render
from urllib.parse import urlencode


# Create your views here.

def microsoft_login(request):
    params = {
        'client_id': settings.MICROSOFT_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': settings.MICROSOFT_REDIRECT_URI,
        'response_mode': 'query',
        'scope': 'openid email profile offline_access',
    }
    url = f"{settings.MICROSOFT_AUTHORIZATION_URL}?{urlencode(params)}"
    return redirect(url)



def microsoft_callback(request):
    code = request.GET.get('code')
    if not code:
        return render(request, 'error.html', {'message': 'No code returned from Microsoft'})

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

    # Benutzerinformationen abrufen
    access_token = token_response_data.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(settings.MICROSOFT_USER_INFO_URL, headers=headers)
    user_info = user_info_response.json()

    # Beispiel: Benutzerinformationen in der Session speichern
    request.session['user'] = {
        'name': user_info.get('displayName'),
        'email': user_info.get('mail') or user_info.get('userPrincipalName'),
    }

    return redirect('/home/inside')
