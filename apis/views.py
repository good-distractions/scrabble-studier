from rest_framework import viewsets, generics, permissions
from flashcard_app import models
from django.contrib.auth.models import User
from .serializers import DictionarySerializer
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token

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
    
class UserDictionaries(generics.ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def get_queryset(self,*args,**kwargs):
        user = Token.objects.filter(*args, **kwargs)
        if user.exists():
            user = user.last().user
            user = models.User.objects.get(username=user)
        print(user)
        # dictionaries = get_objects(models.Dictionary, user = user)
        dictionaries =  models.Dictionary.objects.filter(user=user.pk).all()
        return dictionaries
    
    # queryset = models.Dictionary.objects.all()
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
    
# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = (TokenAuthentication,)
  permission_classes = (AllowAny,)
  def get(self,request,*args,**kwargs):
    print(Token.objects.filter(*args, **kwargs))
    user = Token.objects.filter(*args, **kwargs)
    if user.exists():
        user = user.last().user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# https://www.codersarts.com/post/how-to-create-register-and-login-api-using-django-rest-framework-and-token-authentication
#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer