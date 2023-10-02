from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from flashcard_app import models

class HomeView(TemplateView):
    template_name = 'flashcard_app/index.html'
    
class DictionaryCreateView(LoginRequiredMixin, CreateView):
    model = models.Dictionary
    fields = '__all__'
    success_url = reverse_lazy('portfolio_app:dictionaries')


class DictionaryUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Dictionary
    fields = '__all__'
    # change to take you to dictionary detail
    success_url = reverse_lazy('portfolio_app:dictionaries')


class DictionaryDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Dictionary
    fields = '__all__'
    success_url = reverse_lazy('portfolio_app:dictionaries')


class DictionaryDetailView(DetailView):
    model = models.Dictionary
    fields = '__all__'


class DictionaryListView(ListView):
    model = models.Dictionary
    fields = '__all__'
    context_object_name = 'dictionary_list'