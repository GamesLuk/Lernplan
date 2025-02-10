from django.shortcuts import redirect
from functools import wraps
from system.models import StudentProfile

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

def not_Student(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.session.get('user')
        if not user:
            return redirect("auth:login")  # Redirect if user is not logged in
        student_profile = StudentProfile.objects.filter(school_ID=user.get('school_ID')["school_ID"]).first()
        if not student_profile or student_profile.role == "0":
            return redirect("main:welcome")  # Redirect if role is 0 or profile not found
        return view_func(request, *args, **kwargs)
    return wrapper

def only_students(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.session.get('user')
        if not user:
            return redirect("auth:login")  # Redirect if user is not logged in
        student_profile = StudentProfile.objects.filter(school_ID=user.get('school_ID')["school_ID"]).first()
        if not student_profile or student_profile.role != "0":
            return redirect("main:welcome")  # Redirect if role is not 0 or profile not found
        return view_func(request, *args, **kwargs)
    return wrapper

from django.http import HttpResponseForbidden

def only_localhost(function):
    def wrap(request, *args, **kwargs):
        # Überprüfen, ob der Hostname mit 'localhost' oder '127.0.0.1' beginnt
        host = request.get_host().split(':')[0]  # Der Hostname ohne Port
        if not (host.startswith('localhost') or host.startswith('127.0.0.1')):
            return HttpResponseForbidden("Diese Funktion ist nur von localhost zugänglich.")
        return function(request, *args, **kwargs)
    return wrap