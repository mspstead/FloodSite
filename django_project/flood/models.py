from django.db import models

# Create your models here.

class Photo(models.Model):
    owner = models.TextField()
    title_text = models.TextField()
    date_taken = models.DateTimeField('date taken')
    url = models.TextField()
    lat = models.TextField()
    lng = models.TextField()
    locality = models.TextField()
    source = models.TextField()
    score = models.SmallIntegerField(default=0)

class RainLevel(models.Model):
    date_taken = models.DateTimeField('date taken')
    level = models.TextField()
    reference = models.TextField()
