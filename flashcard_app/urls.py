from django.urls import path
from . import views

app_name = 'flashcard_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dictionary/<int:pk>', views.DictionaryDetailView.as_view(), name='dictionary'),
    path('dictionary/learn/<int:pk>', views.DictionaryStudyView.as_view(), name='study_dictionary'),
    path('dictionaries/', views.DictionaryListView.as_view(), name='dictionaries'),
    path('add_dictionary/', views.DictionaryCreateView.as_view(),
         name='add_dictionary'),
    path('delete_dictionary/<int:pk>', views.DictionaryDeleteView.as_view(), name='delete_dictionary'),
    
]
