from django.urls import path

from .views import DictionaryViewset, UserViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('dictionary',DictionaryViewset, basename="dictionaries" )
router.register('user',UserViewset, basename="users" )
urlpatterns = router.urls