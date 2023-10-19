import django_filters
from .models import Dictionary


class DictionaryFilterSet(django_filters.FilterSet):
    class Meta:
        model = Dictionary
        fields = ['public']