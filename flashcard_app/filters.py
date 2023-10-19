import django_filters
from .models import Dictionary


FILTER_CHOICES = (
    (True, 'Include Public'),
    (False, 'My Dictionaries Only'),
)

# class DictionaryFilterSet(django_filters.FilterSet):
#     public = django_filters.ChoiceFilter(choices=FILTER_CHOICES)

#     class Meta:
#         model = Dictionary
#         fields = ['public']


# https://stackoverflow.com/questions/43009538/use-custom-filter-with-django-modelchoice-filter
class DictionaryFilterSet(django_filters.FilterSet):
    public = django_filters.ChoiceFilter(choices=FILTER_CHOICES, method = 'ids__in')
    
    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super().__init__(data, queryset, request=request, prefix=prefix)
        self.form.initial['public'] = True
        self.user_id = request.user.id
    
    # def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
    #     super(DictionaryFilterSet,self).__init__(data, queryset, request=request, prefix=prefix)
    #     self.user_id = request.user.id      
        
    def ids__in(self, queryset, request, value, *args, **kwargs):
        try:
                if value=='True':
                    queryset = queryset.filter(public=True)|queryset.filter(user=self.user_id)
                elif value=='False':
                    queryset = queryset.filter(user=self.user_id)
        except ValueError:
            pass
            print('except')
        return queryset
    
    class Meta:
        model = Dictionary
        fields = ['public']