from system_control.models import system
from django.conf import settings

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