from django.db import models

class system(models.Model):

    name = models.CharField(max_length=100,db_index=True)
    value = models.CharField(max_length=100,db_index=True)

    def __str__(self):
        return self.name
    
class StudentProfile(models.Model):

    school_ID = models.IntegerField(db_index=True, unique=True, null=True)
    name = models.CharField(max_length=255, db_index=True)
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    teams = models.JSONField(default=list, db_index=True, null=True)  # Speichert eine Liste der Teams des Benutzers
    klasse = models.CharField(max_length=1, db_index=True)
    stufe = models.IntegerField(db_index=True)
    role = models.CharField(max_length=255, db_index=True)
    fächer = models.JSONField(default=list, db_index=True)
    beschreibung = models.TextField(null=True, default=None)
    kürzel = models.CharField(max_length=10, db_index=True, null=True, default=None)

    def __str__(self):
        return self.name
    
class LernzeitProfile(models.Model):

    lernzeit_ID = models.IntegerField(db_index=True)
    fach = models.CharField(max_length=50,db_index=True)
    name = models.CharField(max_length=50,db_index=True)
    type = models.IntegerField(db_index=True)
    klasse = models.CharField(max_length=10, db_index=True, null=True)
    stufen = models.JSONField(db_index=True)
    tag = models.CharField(max_length=20, db_index=True)
    stunde = models.JSONField(db_index=True)
    teacher = models.CharField(max_length=20, db_index=True)
    raum = models.CharField(max_length=10, db_index=True)
    plätze = models.IntegerField(db_index=True)
    beschreibung = models.TextField()
    activ = models.BooleanField(db_index=True)

    def __str__(self):
        return self.name
    
class AnmeldungProfile(models.Model):

    anmeldung_ID = models.IntegerField(db_index=True)
    school_ID = models.IntegerField(db_index=True)
    lernzeit_ID = models.IntegerField(db_index=True)
    date = models.DateField(db_index=True)
    lz_date = models.DateField(db_index=True, default="2021-01-01")
    stunde = models.IntegerField(db_index=True)

    def __str__(self):
        return self.name