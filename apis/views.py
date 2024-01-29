from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider import models
from rest_framework import generics, permissions
from flashcard_app.models import Dictionary
from django.contrib.auth.models import User, Group
from .serializers import DictionarySerializer
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer,RegisterSerializer, GroupSerializer, DictionarySerializer
from rest_framework import generics
from rest_framework.permissions import  AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# https://stackoverflow.com/questions/75001305/how-to-connect-expo-go-app-to-django-rest-framework-backend-on-localhost
@method_decorator(csrf_exempt, name='dispatch')
class UserDictionaries(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = DictionarySerializer    
     
    def get_queryset(self,*args,**kwargs):
        token = self.request.headers['Authorization'].split("Bearer ")[1]
        tokenObj = models.AccessToken.objects.get(token=token)
        user = User.objects.get(username=tokenObj.user)
        dictionaries =  Dictionary.objects.filter(user=user.pk).all()
        return dictionaries

@method_decorator(csrf_exempt, name='dispatch')
class PublicDictionaries(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = DictionarySerializer    
     
    def get_queryset(self,*args,**kwargs):
        dictionaries =  Dictionary.objects.filter(public=True).all()
        return dictionaries

@method_decorator(csrf_exempt, name='dispatch')
class DetailDictionary(generics.RetrieveAPIView):
    queryset = Dictionary.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = DictionarySerializer


# https://www.codersarts.com/post/how-to-create-register-and-login-api-using-django-rest-framework-and-token-authentication
#Class based view to register user
@method_decorator(csrf_exempt, name='dispatch')
class RegisterUserAPIView(generics.CreateAPIView):
  permission_classes = (AllowAny,)
  serializer_class = RegisterSerializer

# class UploadDictionary(generics.CreateAPIView):
@method_decorator(csrf_exempt, name='dispatch')
class UploadDictionary(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def create(self, request):
        file_uploaded = request.FILES.get('file')
        print(file_uploaded)
        data = request.data
        data = {k: v for k, v in data.items()}
        token = self.request.headers['Authorization'].split("Bearer ")[1]
        tokenObj = models.AccessToken.objects.get(token=token)
        user = User.objects.get(username=tokenObj.user)
        newDict = Dictionary.objects.create(title=data["title"],description=data["description"], file = file_uploaded, user = user, public = data["public"]==True)
        newDict.save()
        response = "success!"
        return Response(response)

# Create the API views
class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer