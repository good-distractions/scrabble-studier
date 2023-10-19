from django.urls import path
from . import views

app_name = 'flashcard_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dictionary/<int:pk>', views.DictionaryDetailView.as_view(), name='dictionary'),
    # path('dictionaries', views.DictionaryListView.as_view(), name='dictionaries'),
    path('dictionaries', views.FilteredDictionaryListView.as_view(), name='dictionaries'),
    path('add_dictionary', views.DictionaryCreateView.as_view(),
         name='add_dictionary'),
    path('delete_dictionary/<int:pk>', views.DictionaryDeleteView.as_view(), name='delete_dictionary'),
    path('dictionary/learn/<int:pk>', views.DictionaryStudyAllView.as_view(), name='study_dictionary'),
    path('register/', views.RegisterView.as_view(), name='users-register'),

]
