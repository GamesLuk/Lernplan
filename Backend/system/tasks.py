import threading
import time
from system.models import StudentProfile
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

