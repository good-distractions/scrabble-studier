# apis/urls.py
from django.urls import path

from .views import DictionaryViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('',DictionaryViewset, basename="dictionaries" )
urlpatterns = router.urls