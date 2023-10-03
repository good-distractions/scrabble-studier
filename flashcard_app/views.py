from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from urllib import request
from flashcard_app import models
import pandas as pd
from django.utils.html import format_html


class HomeView(TemplateView):
    template_name = 'flashcard_app/index.html'
    
class DictionaryCreateView(CreateView):
    model = models.Dictionary
    fields = '__all__'
    success_url = reverse_lazy('portfolio_app:dictionaries')


class DictionaryUpdateView(UpdateView):
    model = models.Dictionary
    fields = '__all__'
    # change to take you to dictionary detail
    success_url = reverse_lazy('portfolio_app:dictionaries')


class DictionaryDeleteView(DeleteView):
    model = models.Dictionary
    fields = '__all__'
    success_url = reverse_lazy('portfolio_app:dictionaries')


class DictionaryDetailView(DetailView):
    model = models.Dictionary
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super(DictionaryDetailView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        data = pd.read_csv(self.object.file, header=None)
        # print(data)
        data = data.iloc[:, 0].to_frame().head(5)
        # print(data)
        data.columns=['words']
        print(data)
        context['preview_data'] = data
        return context


class DictionaryListView(ListView):
    model = models.Dictionary
    fields = '__all__'
    context_object_name = 'dictionary_list'
    

class DictionaryStudyView(TemplateView):
    template_name = 'flashcard_app/dictionary_study_view.html'
    # similar to supclub categories, use kwarg to determine filter for annagrams, 
    # words without vowels etc
    
    def get_context_data(self, **kwargs):
        context = super(DictionaryStudyView, self).get_context_data(**kwargs)
        primary_key = super(DictionaryStudyView, self).get_context_data(**kwargs)['pk']
        dictionary = models.Dictionary.objects.get(pk=primary_key)
        context['dictionary'] = dictionary
        data = pd.read_csv(dictionary.file, header=None)
        data = data.iloc[:, 0].head(10)
        print(data)
        print(context)
        return context