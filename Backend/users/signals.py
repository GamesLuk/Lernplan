from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied

@receiver(user_logged_in)
def check_email_domain(sender, request, user, **kwargs):

    allowed_domains = ['lmg.schulen-lev.de']  # Erlaubte Domains

    email_domain = user.email.split('@')[-1]  # Domain extrahieren

    if email_domain not in allowed_domains:
        logout(request)  # Benutzer sofort ausloggen

        raise PermissionDenied("Nur E-Mail-Adressen bestimmter Domains sind erlaubt.")
