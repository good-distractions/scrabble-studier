from django.urls import path

from .views import DictionaryViewset, UserDetail, UserList, ListDictionary, DetailDictionary
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('dictionary',DictionaryViewset, basename="dictionaries" )
# router.register('user',UserViewset, basename="users" )
# urlpatterns = router.urls

urlpatterns = [
    path('dictionary/', ListDictionary.as_view()),
    path('dictionary/<int:pk>/', DetailDictionary.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
    path('user/', UserList.as_view())
]