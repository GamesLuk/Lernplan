from django.db import models

class system(models.Model):

    name = models.CharField(max_length=100,db_index=True)
    value = models.CharField(max_length=100,db_index=True)

    def __str__(self):
        return self.name
    
class StudentProfile(models.Model):
    school_ID = models.IntegerField(db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    profile_picture = models.BinaryField(null=True, blank=True, db_index=True)  # Das Bild wird binär gespeichert
    teams = models.JSONField(default=list, db_index=True)  # Speichert eine Liste der Teams des Benutzers
    klasse = models.CharField(max_length=1, db_index=True)
    stufe = models.IntegerField(db_index=True)

    def __str__(self):
        return self.name