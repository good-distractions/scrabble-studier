from typing import Any
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


# class DictionaryDetailView(Form,FormMixin):
#     model = models.Dictionary
#     fields = '__all__'
#     form_class = CustomFilterForm
#     success_url = reverse_lazy('flashcard_app:study_dictionary', args=[2])
    
#     def get_context_data(self, **kwargs):
#         context = super(DictionaryDetailView, self).get_context_data(**kwargs)
#         self.object = self.get_object()
#         data = pd.read_csv(self.object.file, header=None)
#         data = data.iloc[:, 0].to_frame().head(5)
#         data.columns = ['words']
#         context['preview_data'] = data
#         # print(context)
#         # print(self.get_success_url())
#         return context

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
        # return reverse_lazy('flashcard_app:study_dictionary', args=(self.object.id,))
        return reverse_lazy('flashcard_app:study_dictionary', args=(self.object.id,filter_type,substring,word_length))

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
            # print('valid')
            return self.form_valid(form)
        else:
            # print('invalid')
            return self.form_invalid(form)

    def form_valid(self, form):
        self.form = form.cleaned_data
        return super(DictionaryDetailView, self).form_valid(form)
    # https://stackoverflow.com/questions/47623088/detailview-object-relations    

# # class DictionaryDetailView(FormView):
#     form_class = CustomFilterForm
#     template_name = 'flashcard_app/dictionary_detail.html'
#     # success_url = reverse_lazy('flashcard_app:dictionaries', 2)
    
#     # def get_form_kwargs(self):
#     #     kwargs = super(DictionaryDetailView,self).get_form_kwargs()
#     #     # kwargs['request'] = self.request
#     #     print(kwargs)
#     #     return kwargs
    
#     def get_context_data(self, **kwargs):
#         context = super(DictionaryDetailView,self).get_context_data(**kwargs)
#         print(context)
#         context['dictionary'] = self.get_object_or_404(models.Dictionary, self.kwargs['pk'])
#         return super(DictionaryDetailView,self).get_context_data(**kwargs)
    
#     def form_valid(self,form):
#         pass
#         return super(DictionaryDetailView, self).form_valid(form)
    
#     def get_success_url(self, **kwargs):
#         context = super(DictionaryDetailView,self).get_context_data(**kwargs)
#         form_data = self.form
#         context['form_data'] = form_data
#         primary_key = context['dictionary'].pk
#         return reverse_lazy('flashcard_app:study_dictionary',args=[primary_key])
#         # return reverse_lazy('flashcard_app:study_dictionary',
#         #                     args = [self.object.pk,
#         #                             form_data['filter_type'],
#         #                             form_data['substring'],
#         #                             form_data['word_length']])
#         # return reverse_lazy('flashcard_app:study_dictionary',
#         #             kwargs = {'pk':self.object.pk,
#         #                 'filter_type':form_data['filter_type'],
#         #                 'word_length':form_data['word_length'],
#         #                 'substring':form_data['substring']})
    

class DictionaryListView(ListView):
    model = models.Dictionary
    fields = '__all__'
    context_object_name = 'dictionary_list'


class DictionaryStudyAllView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyAllView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudyQNoUView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyQNoUView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        data = data[data.str.contains('q', case=False, na=False)]
        data = data[~data.str.contains('u', case=False, na=False)]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudyPalindromesView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyPalindromesView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = pd.DataFrame(data.iloc[:, 0])
        data.columns = ['word']
        data['rev'] = data['word'].str[::-1]
        data = data[data['rev']==data['word']]
        data = data.iloc[:, 0]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudyNoVowelsView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyNoVowelsView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        data = data[data.str.count(r'[aeiou]') == 0]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudy7L5VsView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudy7L5VsView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        data = data[data.str.contains('q', case=False, na=False)]
        data = data[~data.str.contains('u', case=False, na=False)]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudy5L4VsView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudy5L4VsView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        data = data[data.str.len() == 5]
        data = data[data.str.count(r'[aeiou]') == 4]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudySatineView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudySatineView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        data = data[data.str.len() == 7]
        data = data[data.str.contains('s', case=False, na=False)]
        data = data[~data.str.contains('a', case=False, na=False)]
        data = data[~data.str.contains('t', case=False, na=False)]
        data = data[~data.str.contains('i', case=False, na=False)]
        data = data[~data.str.contains('n', case=False, na=False)]
        data = data[~data.str.contains('e', case=False, na=False)]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudyEndInZView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyEndInZView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        data = data[data.str.endswith('z', case=False, na=False)]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudyXLetterContainZView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyXLetterContainZView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        data = data[data.str.len() == 3]
        data = data[data.str.contains('z', case=False, na=False)]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudyXLettersView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyXLettersView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        data = data[data.str.len() == 3]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context


class DictionaryStudyContainXYZView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'

    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyContainXYZView,
                        self).get_context_data(**kwargs)
        primary_key = context['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0]
        # data = data[data.str.contains('xy', case=False, na=False)]
        data = data.values.tolist()
        context['my_data'] = json.dumps(data)
        return context
