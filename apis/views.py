# apis/views.py
from rest_framework import viewsets

from flashcard_app import models
from django.contrib.auth.models import User
from .serializers import DictionarySerializer
from .serializers import UserSerializer

class DictionaryViewset(viewsets.ModelViewSet):
    queryset = models.Dictionary.objects.all()
    serializer_class = DictionarySerializer
    
class UserViewset(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer