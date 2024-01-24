from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider import models
from rest_framework import viewsets, generics, permissions
from flashcard_app.models import Dictionary
from django.contrib.auth.models import User, Group
from .serializers import DictionarySerializer
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,RegisterSerializer, GroupSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class DictionaryViewset(viewsets.ModelViewSet):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    
class ListDictionary(generics.ListCreateAPIView):
    queryset = Dictionary.objects.all()
    serializer_class = DictionarySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
# class UserDictionaries(generics.ListCreateAPIView):
#     serializer_class = UserSerializer
    
#     def get_queryset(self,*args,**kwargs):
#         user = self.request.user
#         print(user)
#         if user.exists():
#             user = user.last().user
#             user = User.objects.get(username=user)
#         # dictionaries = get_objects(Dictionary, user = user)
#         dictionaries =  Dictionary.objects.filter(user=user.pk).all()
#         return dictionaries
    
class UserDictionaries(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = DictionarySerializer    
     
    def get_queryset(self,*args,**kwargs):
        token = self.request.headers ['Authorization'].split("Bearer ")[1]
        tokenObj = models.AccessToken.objects.get(token=token)
        print(tokenObj.user)
        user = User.objects.get(username=tokenObj.user)
        dictionaries =  Dictionary.objects.filter(user=user.pk).all()
        print(dictionaries)
        return dictionaries
    

    
class UploadDictionary(generics.CreateAPIView):
    serializer_class = DictionarySerializer
    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def create(self, request, *args, **kwargs):
        user = Token.objects.filter(*args, **kwargs)
        if user.exists():
            user = user.last().user
            user = User.objects.get(username=user)

        Dictionary.objects.create()
    

class DetailDictionary(generics.RetrieveAPIView):
    queryset = Dictionary.objects.all()
    [SessionAuthentication, TokenAuthentication]
    serializer_class = DictionarySerializer
    
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context["customer_id"] = self.kwargs['customer_id']
    #     context["query_params"] = self.request.query_params
    #     return context
    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class=UserSerializer
    
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class=UserSerializer
    

# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
  authentication_classes = [SessionAuthentication, TokenAuthentication]
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