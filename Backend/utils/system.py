from system.models import system
from django.conf import settings
from datetime import datetime

def getSchool_ID():
    id = system.objects.filter(name="ID").values("value").first()

    if not id:
        id = system.objects.create(
            name="ID",
            value="10000"
        )
    
    school_ID = id["value"]
    system.objects.update(
        value=int(school_ID) + 1
    )
    return school_ID

def debug(message):
    for text in message:
        print(text)

def getKlasse(school_ID):
    month = datetime.now().month
    day = datetime.now().day

    if month >= 8:
        year = datetime.now().year + "-" + (datetime.now().year + 1)
    else:
        year = (datetime.now().year - 1) + "-" + datetime.now().year