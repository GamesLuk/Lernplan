from django.shortcuts import redirect
from functools import wraps

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        to = request.get_host()
        request.session["requested_url"] = to
        # Prüfen, ob der Benutzer eingeloggt ist
        if not request.session.get('logged_in'):
            return redirect("auth:login")  # Falls nicht eingeloggt, weiterleiten
        return view_func(request, *args, **kwargs)  # Falls eingeloggt, die View ausführen
    return wrapper

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.session.get('user')
            if not user or user.get('role') != role:
                previous_url = request.META.get('HTTP_REFERER', '/home/')
                return redirect(previous_url)  # Weiterleiten, wenn Rolle nicht passt
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator