from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from . import models
import pandas as pd
from django.utils.html import format_html
import json
from .forms import CustomFilterForm
from urllib.parse import urlencode


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

class DictionaryListView(ListView):
    model = models.Dictionary
    fields = '__all__'
    context_object_name = 'dictionary_list'

class DictionaryDetailView(DetailView, FormMixin):
    model = models.Dictionary
    fields = '__all__'
    form_class = CustomFilterForm
    
    def get_context_data(self, **kwargs):
        context = super(DictionaryDetailView, self).get_context_data(**kwargs)
        context['filter_form'] = CustomFilterForm(initial = {'post':self.object})
        self.object = self.get_object()
        data = pd.read_csv(self.object.file, header=None)
        # print(data)
        data = data.iloc[:, 0].to_frame().head(5)
        # print(data)
        data.columns = ['words']
        # print(data)
        context['preview_data'] = data
        return context
    
    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form.cleaned_data)
    #     else:
    #         return self.form_invalid(form)

    # def form_valid(self, form):
    #     self.form = form
    #     return super(DictionaryDetailView, self).form_valid(form)
    
    # def form_valid(self, form):
    #     context = self.get_context_data(form=form)
    #     # print(context)
    #     return self.render_to_response(context=context)
    
    # def get_success_url(self, **kwargs):
    #     context = super(DictionaryDetailView,self).get_context_data(**kwargs)
    #     form_data = self.form
    #     # print(form_data['filter_type'])
    #     context['form_data'] = form_data
    #     primary_key = context['dictionary'].pk
    #     # return reverse_lazy('flashcard_app:study_dictionary',args=[primary_key])
    #     # return reverse_lazy('flashcard_app:study_dictionary',
    #     #                     args = [self.object.pk,
    #     #                             form_data['filter_type'],
    #     #                             form_data['substring'],
    #     #                             form_data['word_length']])
    #     return reverse_lazy('flashcard_app:study_dictionary',
    #                 kwargs = {'pk':self.object.pk,
    #                     'filter_type':form_data['filter_type'],
    #                     'word_length':form_data['word_length'],
    #                     'substring':form_data['substring']})


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
