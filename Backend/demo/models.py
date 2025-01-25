from django.db import models

# Create your models here.

class TestData(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    age = models.IntegerField(db_index=True)