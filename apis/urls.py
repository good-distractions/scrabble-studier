from django.urls import path
from rest_framework.authtoken import views
from .views import UploadDictionary, UserDictionaries, UserDetails, GroupList,UserDetailAPI,RegisterUserAPIView,UserDetail, UserList, ListDictionary, DetailDictionary

urlpatterns = [
    path('dictionary/', ListDictionary.as_view()),
    path('dictionary/upload/', UploadDictionary.as_view()),
    path('dictionary/<int:pk>/', DetailDictionary.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
    path('user/', UserList.as_view()),
    path('user_dictionaries/', UserDictionaries.as_view()),
    path('api-token-auth/', views.obtain_auth_token),
    path("user/details",UserDetailAPI.as_view()),
    path('user/register',RegisterUserAPIView.as_view()),
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('groups/', GroupList.as_view()),
]
