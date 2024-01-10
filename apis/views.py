from rest_framework import viewsets, generics, permissions
from flashcard_app import models
from django.contrib.auth.models import User
from .serializers import DictionarySerializer
from .serializers import UserSerializer

class DictionaryViewset(viewsets.ModelViewSet):
    queryset = models.Dictionary.objects.all()
    serializer_class = DictionarySerializer
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class=UserSerializer
    
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class=UserSerializer
    
class ListDictionary(generics.ListCreateAPIView):
    queryset = models.Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class DetailDictionary(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class DetailDictionary(generics.RetrieveAPIView):
    queryset = models.Dictionary.objects.all()
    
    serializer_class = DictionarySerializer
    
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context["customer_id"] = self.kwargs['customer_id']
    #     context["query_params"] = self.request.query_params
    #     return context