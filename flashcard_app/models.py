from django.db import models
from django.urls import reverse
import pathlib

class Dictionary(models.Model):
    title = models.CharField(max_length=60)
    source = models.URLField( max_length=400,blank=True, default=True,null=True)
    file = models.FileField(blank=False, null=False)