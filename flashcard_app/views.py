from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView,FormView
from django.urls import reverse, reverse_lazy
from urllib import request
from flashcard_app import models
import pandas as pd
from django.utils.html import format_html
import json
from django.http import HttpResponse
from .forms import CustomFilterForm
from django.views.generic.edit import FormMixin, SingleObjectMixin



class HomeView(TemplateView):
    template_name = 'flashcard_app/index.html'


class DictionaryCreateView(CreateView):
    model = models.Dictionary
    fields = '__all__'
    success_url = reverse_lazy('flashcard_app:dictionaries')


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
        # print('context')
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
    

class DictionaryListView(ListView):
    model = models.Dictionary
    fields = '__all__'
    context_object_name = 'dictionary_list'


class DictionaryStudyAllView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'
    
    def post(self, request,pk,*args, **kwargs):
        post_values = request.session.get('POSTVALUES')  
        self.request.session.modified = True
        return super(DictionaryStudyAllView,self).get(request, args=[pk])

        
    # def get(self, request, *args, **kwargs):
    #     post_values = request.session.get('POSTVALUES')  
    #     print(post_values)

    # def post(self, request, *args, **kwargs):
    #     post_values = request.session.get('POSTVALUES')  
    #     return
    
    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyAllView,
                        self).get_context_data(**kwargs)
        # figure out how to clear
        # filter_vals = self.request.session.get('POSTVALUES')
        # print(self.request.session.get('POSTVALUES'))
        # print(self.request.POST)
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
        # print(self.request.POST) 
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
        # self.request.session.delete('POSTVALUES')
        # del self.request.session["POSTVALUES"]
        # self.request.session.modified = True
        return context


# class DictionaryStudyQNoUView(TemplateView):
#     template_name = 'flashcard_app/dictionary_study_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(DictionaryStudyQNoUView,
#                         self).get_context_data(**kwargs)
#         primary_key = context['pk']
#         dictionary = models.Dictionary.objects.get(pk=primary_key)
#         context['dictionary'] = dictionary
#         data = pd.read_csv(dictionary.file, header=None)
#         data = data.iloc[:, 0]
#         data = data[data.str.contains('q', case=False, na=False)]
#         data = data[~data.str.contains('u', case=False, na=False)]
#         data = data.values.tolist()
#         context['my_data'] = json.dumps(data)
#         return context


# class DictionaryStudyPalindromesView(TemplateView):
#     template_name = 'flashcard_app/dictionary_study_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(DictionaryStudyPalindromesView,
#                         self).get_context_data(**kwargs)
#         primary_key = context['pk']
#         dictionary = models.Dictionary.objects.get(pk=primary_key)
#         context['dictionary'] = dictionary
#         data = pd.read_csv(dictionary.file, header=None)
#         data = pd.DataFrame(data.iloc[:, 0])
#         data.columns = ['word']
#         data['rev'] = data['word'].str[::-1]
#         data = data[data['rev']==data['word']]
#         data = data.iloc[:, 0]
#         data = data.values.tolist()
#         context['my_data'] = json.dumps(data)
#         return context


# class DictionaryStudyNoVowelsView(TemplateView):
#     template_name = 'flashcard_app/dictionary_study_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(DictionaryStudyNoVowelsView,
#                         self).get_context_data(**kwargs)
#         primary_key = context['pk']
#         dictionary = models.Dictionary.objects.get(pk=primary_key)
#         context['dictionary'] = dictionary
#         data = pd.read_csv(dictionary.file, header=None)
#         data = data.iloc[:, 0]
#         data = data[data.str.count(r'[aeiou]') == 0]
#         data = data.values.tolist()
#         context['my_data'] = json.dumps(data)
#         return context


# class DictionaryStudy7L5VsView(TemplateView):
#     template_name = 'flashcard_app/dictionary_study_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(DictionaryStudy7L5VsView,
#                         self).get_context_data(**kwargs)
#         primary_key = context['pk']
#         dictionary = models.Dictionary.objects.get(pk=primary_key)
#         context['dictionary'] = dictionary
#         data = pd.read_csv(dictionary.file, header=None)
#         data = data.iloc[:, 0]
#         data = data[data.str.contains('q', case=False, na=False)]
#         data = data[~data.str.contains('u', case=False, na=False)]
#         data = data.values.tolist()
#         context['my_data'] = json.dumps(data)
#         return context


# class DictionaryStudy5L4VsView(TemplateView):
#     template_name = 'flashcard_app/dictionary_study_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(DictionaryStudy5L4VsView,
#                         self).get_context_data(**kwargs)
#         primary_key = context['pk']
#         dictionary = models.Dictionary.objects.get(pk=primary_key)
#         context['dictionary'] = dictionary
#         data = pd.read_csv(dictionary.file, header=None)
#         data = data.iloc[:, 0]
#         data = data[data.str.len() == 5]
#         data = data[data.str.count(r'[aeiou]') == 4]
#         data = data.values.tolist()
#         context['my_data'] = json.dumps(data)
#         return context


# class DictionaryStudySatineView(TemplateView):
#     template_name = 'flashcard_app/dictionary_study_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(DictionaryStudySatineView,
#                         self).get_context_data(**kwargs)
#         primary_key = context['pk']
#         dictionary = models.Dictionary.objects.get(pk=primary_key)
#         context['dictionary'] = dictionary
#         data = pd.read_csv(dictionary.file, header=None)
#         data = data.iloc[:, 0]
#         data = data[data.str.len() == 7]
#         data = data[data.str.contains('s', case=False, na=False)]
#         data = data[~data.str.contains('a', case=False, na=False)]
#         data = data[~data.str.contains('t', case=False, na=False)]
#         data = data[~data.str.contains('i', case=False, na=False)]
#         data = data[~data.str.contains('n', case=False, na=False)]
#         data = data[~data.str.contains('e', case=False, na=False)]
#         data = data.values.tolist()
#         context['my_data'] = json.dumps(data)
#         return context


# class DictionaryStudyEndInZView(TemplateView):
#     template_name = 'flashcard_app/dictionary_study_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(DictionaryStudyEndInZView,
#                         self).get_context_data(**kwargs)
#         primary_key = context['pk']
#         dictionary = models.Dictionary.objects.get(pk=primary_key)
#         context['dictionary'] = dictionary
#         data = pd.read_csv(dictionary.file, header=None)
#         data = data.iloc[:, 0]
#         data = data[data.str.endswith('z', case=False, na=False)]
#         data = data.values.tolist()
#         context['my_data'] = json.dumps(data)
#         return context


# class DictionaryStudyXLetterContainZView(TemplateView):
#     template_name = 'flashcard_app/dictionary_study_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(DictionaryStudyXLetterContainZView,
#                         self).get_context_data(**kwargs)
#         primary_key = context['pk']
#         dictionary = models.Dictionary.objects.get(pk=primary_key)
#         context['dictionary'] = dictionary
#         data = pd.read_csv(dictionary.file, header=None)
#         data = data.iloc[:, 0]
#         data = data[data.str.len() == 3]
#         data = data[data.str.contains('z', case=False, na=False)]
#         data = data.values.tolist()
#         context['my_data'] = json.dumps(data)
#         return context


# class DictionaryStudyXLettersView(TemplateView):
#     template_name = 'flashcard_app/dictionary_study_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(DictionaryStudyXLettersView,
#                         self).get_context_data(**kwargs)
#         primary_key = context['pk']
#         dictionary = models.Dictionary.objects.get(pk=primary_key)
#         context['dictionary'] = dictionary
#         data = pd.read_csv(dictionary.file, header=None)
#         data = data.iloc[:, 0]
#         data = data[data.str.len() == 3]
#         data = data.values.tolist()
#         context['my_data'] = json.dumps(data)
#         return context


# class DictionaryStudyContainXYZView(TemplateView):
    # template_name = 'flashcard_app/dictionary_study_view.html'

    # def get_context_data(self, **kwargs):
    #     context = super(DictionaryStudyContainXYZView,
    #                     self).get_context_data(**kwargs)
    #     primary_key = context['pk']
    #     dictionary = models.Dictionary.objects.get(pk=primary_key)
    #     context['dictionary'] = dictionary
    #     data = pd.read_csv(dictionary.file, header=None)
    #     data = data.iloc[:, 0]
    #     # data = data[data.str.contains('xy', case=False, na=False)]
    #     data = data.values.tolist()
    #     context['my_data'] = json.dumps(data)
    #     return context
