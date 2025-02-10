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

def getLernzeit_ID():
    id = system.objects.filter(name="lernzeit_ID").values("value").first()

    if not id:
        id = system.objects.create(
            name="lernzeit_ID",
            value="1"
        )
    
    lernzeit_ID = id["value"]
    system.objects.update(
        value=int(lernzeit_ID) + 1
    )
    return lernzeit_ID

def getAnmeldung_ID():
    id = system.objects.filter(name="anmeldung_ID").values("value").first()

    if not id:
        id = system.objects.create(
            name="anmeldung_ID",
            value="1"
        )
    
    anmeldung_ID = id["value"]
    system.objects.update(
        value=int(anmeldung_ID) + 1
    )
    return anmeldung_ID


def debug(message):
    for text in message:
        print(text)

def setKlasse_Role(school_IDx):
    month = datetime.now().month

    if month >= 8:
        year = str(datetime.now().year)[-2:] + "-" + str(datetime.now().year + 1)[-2:]
    else:
        year = str(datetime.now().year - 1)[-2:] + "-" + str(datetime.now().year)[-2:]

    name = year + " Klasse "

    teams = getStudent("school_ID", school_IDx, "teams")

    role = 0

    StudentProfile.objects.filter(school_ID=school_IDx).update(role=role)

    for team in teams:
        if team["displayName"].startswith("Kollegium"):
            role = 2
            StudentProfile.objects.filter(school_ID=school_IDx).update(role=role)

        if role != 0:
            return

        if team["displayName"].startswith(name):
            stufe = team["displayName"].split("e ", 1)[1][:2]
            klasse = team["displayName"].split(stufe, 1)[1][:1]

            StudentProfile.objects.filter(school_ID=school_IDx).update(stufe=stufe)
            StudentProfile.objects.filter(school_ID=school_IDx).update(klasse=klasse)

    # All - alle die nicht -> name - preset -> Klasse

def getStudent(filter, parameter, value):
    if filter == "school_ID":
        return StudentProfile.objects.filter(school_ID=parameter).values(value).first()[value]
    elif filter == "email":
        return StudentProfile.objects.filter(email=parameter).values(value).first()[value]
    
def getDay():
    return datetime.now().day
