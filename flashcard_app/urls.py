from django.urls import path
from . import views

app_name = 'flashcard_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('upload/', views.UploadView.as_view(), name='upload')
]
