from system.models import system
from django.conf import settings
from datetime import datetime
from system.models import StudentProfile

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

def setKlasse(school_IDx):
    month = datetime.now().month

    if month >= 8:
        year = str(datetime.now().year)[-2:] + "-" + str(datetime.now().year + 1)[-2:]
    else:
        year = str(datetime.now().year - 1)[-2:] + "-" + str(datetime.now().year)[-2:]

    name = year + " Klasse "

    teams = StudentProfile.objects.filter(school_ID=school_IDx).values("teams").first()["teams"]

    for team in teams:
        if team["displayName"].startswith(name):
            stufe = team["displayName"].split("e ", 1)[1][:2]
            klasse = team["displayName"].split(stufe, 1)[1][:1]

            StudentProfile.objects.filter(school_ID=school_IDx).update(stufe=stufe)
            StudentProfile.objects.filter(school_ID=school_IDx).update(klasse=klasse)

    # All - alle die nicht -> name - preset -> Klasse