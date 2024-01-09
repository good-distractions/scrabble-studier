# apis/views.py
from rest_framework import viewsets

from flashcard_app import models
from .serializers import DictionarySerializer

class DictionaryViewset(viewsets.ModelViewSet):
    queryset = models.Dictionary.objects.all()
    serializer_class = DictionarySerializer