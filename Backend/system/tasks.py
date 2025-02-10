import threading
import time
from system.models import StudentProfile, LernzeitProfile, system, AnmeldungProfile, 
from utils.system import setKlasse_Role

def set_Klasse_Role():
    while True:
        for school_ID in StudentProfile.objects.values_list("school_ID", flat=True).distinct():
            setKlasse_Role(school_ID)
        time.sleep(1*60*60*24*7)

def start_task(task):
    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()

#-----------------------------------------------------------------------------------------------#

from celery import shared_task
from django.core.cache import cache
from .models import LernzeitProfile

@shared_task
def update_cache():
    print("🔄 Aktualisiere Cache mit Datenbank...")
    data = list(

        LernzeitProfile.objects.all(),
        StudentProfile.objects.all(),
        system.objects.all(),
        AnmeldungProfile.objects.all()
        
        )  # Datenbankabfrage
    cache.set("mymodel_queryset", data, timeout=300)  # 15 Min Cache
    print("✅ Cache aktualisiert!")