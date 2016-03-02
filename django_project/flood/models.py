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
