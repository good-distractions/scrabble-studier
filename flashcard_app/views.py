from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, DetailView, ListView, UpdateView, DeleteView
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
        context['data'] = data
        return context


class DictionaryListView(ListView):
    model = models.Dictionary
    fields = '__all__'
    context_object_name = 'dictionary_list'
    
