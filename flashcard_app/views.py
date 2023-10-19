from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from flashcard_app import models
import pandas as pd
from flashcard_app.filters import DictionaryFilterSet
from django_filters.views import FilterView
import json
from django.contrib import messages
from django.shortcuts import render,redirect
from .forms import CustomFilterForm,RegisterForm
from django.views.generic.edit import FormMixin



class HomeView(TemplateView):
    template_name = 'flashcard_app/index.html'


class DictionaryCreateView(CreateView):
    model = models.Dictionary
    fields = '__all__'
    success_url = reverse_lazy('flashcard_app:dictionaries')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DictionaryCreateView, self).form_valid(form)


class DictionaryUpdateView(UpdateView):
    model = models.Dictionary
    fields = '__all__'
    # change to take you to dictionary detail
    success_url = reverse_lazy('flashcard_app:dictionaries')


class DictionaryDeleteView(DeleteView):
    model = models.Dictionary
    fields = '__all__'
    success_url = reverse_lazy('flashcard_app:dictionaries')


class DictionaryDetailView(DetailView, FormMixin):
    model = models.Dictionary
    fields = '__all__'
    # https://stackoverflow.com/questions/45659986/django-implementing-a-form-within-a-generic-detailview
    form_class = CustomFilterForm

    def get_success_url(self):
        form = self.form
        filter_type = self.form['filter_type']
        substring = self.form['substring']
        word_length = self.form['word_length']
        print(form)
        return reverse_lazy('flashcard_app:study_dictionary', args=(self.object.id,))
        # return reverse_lazy('flashcard_app:study_dictionary_qnou', kwargs={'pk':self.object.id,'filter_type':filter_type,'word_length':word_length,'substring':substring})

    def get_context_data(self, **kwargs):
        context = super(DictionaryDetailView, self).get_context_data(**kwargs)
        context['form'] = CustomFilterForm()
        data = pd.read_csv(self.object.file, header=None)
        data = data.iloc[:, 0]
        data = pd.DataFrame(data)
        data.columns = ['word']
        context['preview_data'] = data.head(5)
        print(context['preview_data'])
        return context

    def post(self, request, *args, **kwargs):
        # print('post')
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid() and request.POST.get("form_type"):
            print(request.POST.copy())
            request.session['POSTVALUES'] = request.POST.copy()
            request.session.modified = True
            print(request.session['POSTVALUES'])
            return self.form_valid(form)
        else:
            # print('invalid')
            return self.form_invalid(form)

    def form_valid(self, form):
        self.form = form.cleaned_data
        return super(DictionaryDetailView, self).form_valid(form)
    # https://stackoverflow.com/questions/47623088/detailview-object-relations    
    
class PublicDictionaryListView(ListView):
    model = models.Dictionary
    fields = '__all__'
    context_object_name = 'dictionary_list'
    template_name ='flashcard_app/public_dictionary_list.html'

class DictionaryListView(ListView):
    model = models.Dictionary
    fields = '__all__'
    context_object_name = 'dictionary_list'
    
# https://stackoverflow.com/questions/59480402/how-to-use-django-filter-with-a-listview-class-view-for-search

class FilteredDictionaryListView(FilterView):
    model = models.Dictionary
    fields = '__all__'
    context_object_name = 'dictionary_list'
    filterset_class = DictionaryFilterSet
    template_name = 'flashcard_app/dictionary_list.html'

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        queryset = queryset.filter(public=True)|queryset.filter(user=self.request.user.id)
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET,queryset=queryset, request=self.request)
        # Return the filtered queryset
        return self.filterset.qs.distinct()



class DictionaryStudyAllView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'
    
    def post(self, request,pk,*args, **kwargs):
        post_values = request.session.get('POSTVALUES')  
        self.request.session.modified = True
        return super(DictionaryStudyAllView,self).get(request, args=[pk])
    
    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyAllView,
                        self).get_context_data(**kwargs)
        filter_vals = {}
        filter_vals['filter_type'] = self.request.POST['filter_type']
        # print(filter_vals)
        filter_vals['substring'] = self.request.POST['substring']
        filter_vals['word_length'] = self.request.POST['word_length']
        primary_key = context['args'][0]
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        print(filter_vals)
        if filter_vals['filter_type']== 'all':
            pass
        elif filter_vals['filter_type']== 'q_no_u':
            data = data[data.str.contains('q', case=False, na=False)]
            data = data[~data.str.contains('u', case=False, na=False)]
        elif filter_vals['filter_type']== 'palindrome':
            data = pd.DataFrame(data)
            data.columns = ['word']
            data['rev'] = data['word'].str[::-1]
            data = data[data['rev']==data['word']]
            data = data.iloc[:, 0]
        elif filter_vals['filter_type']== '7l5v':
            data = data[data.str.len() == 7]
            data = data[data.str.count(r'[aeiouAEIOU]') == 5]
        elif filter_vals['filter_type']== '5l4v':
            data = data[data.str.len() == 5]
            data = data[data.str.count(r'[aeiouAEIOU]') == 4]
        elif filter_vals['filter_type']== 'satine':
            data = data[data.str.len() == 7]
            data = data[data.str.contains('s', case=False, na=False)]
            data = data[data.str.contains('a', case=False, na=False)]
            data = data[data.str.contains('t', case=False, na=False)]
            data = data[data.str.contains('i', case=False, na=False)]
            data = data[data.str.contains('n', case=False, na=False)]
            data = data[data.str.contains('e', case=False, na=False)]
        elif filter_vals['filter_type']== 'endinz':
            data = data[data.str.endswith('z')|data.str.endswith('Z')]
        elif filter_vals['filter_type']== 'no_vowels':
            print('no_vowels')
            data = data[data.str.count(r'[aeiouAEIOU]') == 0]
        if filter_vals['word_length'] !='':
            data = data[data.str.len() == int(filter_vals['word_length'])]
        if filter_vals['substring'] != '':
            data = data[data.str.contains(filter_vals['substring'], case=False, na=False)]
        print(data.head(10))
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context
    
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})       
