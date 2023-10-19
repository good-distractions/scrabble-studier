from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


class Dictionary(models.Model):
    title = models.CharField(max_length=60)
    source = models.URLField( max_length=400,blank=True,null=True)
    file = models.FileField(blank=False, null=False,validators=[FileExtensionValidator(allowed_extensions=["csv"])])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)