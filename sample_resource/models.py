from django.db import models

# Create your models here.

class SampleResource(models.Model):
    text = models.CharField(max_length=100)
    figure = models.IntegerField()
