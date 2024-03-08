from django.urls import path
from .views import UploadDictionary, UserDictionaries, PublicDictionaries,GroupList,RegisterUserAPIView, DetailDictionary, DetailDictionaryFull,DeleteUserAPIView,UserDetails

urlpatterns = [
    path('dictionary/upload/', UploadDictionary.as_view()),
    path('dictionary/<int:pk>/', DetailDictionary.as_view()),
     path('dictionary/full/<int:pk>/', DetailDictionaryFull.as_view()),
    path('user_dictionaries/', UserDictionaries.as_view()),
    path('public_dictionaries/', PublicDictionaries.as_view()),
    path('user/register/',RegisterUserAPIView.as_view()),
    path('user/delete/',DeleteUserAPIView.as_view()),
    path('user/details/',UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
]
