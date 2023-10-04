# https://dev.to/earthcomfy/creating-the-sign-up-page-part-ii-5a3a
from django import forms
from .models import Profile, Location, Interest, Post



class CustomFilterForm(forms.ModelForm):
    # avatar = forms.ImageField(widget=forms.FileInput())
    substring = forms.CharField(widget=forms.Textarea())
    word_length = forms.IntegerField(widget=forms.NumberInput())

    def __init__(self, *args, **kwargs):
        super(CustomFilterForm, self).__init__(*args, **kwargs)
        self.fields['substring'].required = False
        self.fields['word_length'].required = False
