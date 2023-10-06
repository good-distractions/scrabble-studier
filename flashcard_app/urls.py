from django.urls import path
from . import views

app_name = 'flashcard_app'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('dictionary/<int:pk>', views.DictionaryDetailView.as_view(), name='dictionary'),
    path('dictionaries', views.DictionaryListView.as_view(), name='dictionaries'),
    path('add_dictionary', views.DictionaryCreateView.as_view(),
         name='add_dictionary'),
    path('delete_dictionary/<int:pk>', views.DictionaryDeleteView.as_view(), name='delete_dictionary'),
    path('dictionary/learn/<int:pk>', views.DictionaryStudyAllView.as_view(), name='study_dictionary'),
    path('dictionary/learn/q_no_u/<int:pk>', views.DictionaryStudyQNoUView.as_view(), name='study_dictionary_qnou'),
    # path('dictionary/learn/5l4v/<int:pk>', views.DictionaryStudy5L4VsView.as_view(), name='study_dictionary_5l4v'),
    # path('dictionary/learn/7l5v/<int:pk>', views.DictionaryStudy7L5VsView.as_view(), name='study_dictionary_7l5v'),
    # path('dictionary/learn/xyz/<int:pk>', views.DictionaryStudyContainXYZView.as_view(), name='study_dictionary_xyz'),
    # path('dictionary/learn/endinz/<int:pk>', views.DictionaryStudyEndInZView.as_view(), name='study_dictionary_endinz'),
    # path('dictionary/learn/novowels/<int:pk>', views.DictionaryStudyNoVowelsView.as_view(), name='study_dictionary_novowels'),
    # path('dictionary/learn/palindrome/<int:pk>', views.DictionaryStudyPalindromesView.as_view(), name='study_dictionary_palindrome'),
    # path('dictionary/learn/satine/<int:pk>', views.DictionaryStudySatineView.as_view(), name='study_dictionary_satine'),
    # path('dictionary/learn/xlcontainz/<int:pk>', views.DictionaryStudyXLetterContainZView.as_view(), name='study_dictionary_xlcontainz'),
    # path('dictionary/learn/xlw/<int:pk>', views.DictionaryStudyXLettersView.as_view(), name='study_dictionary_xlw'),
]
