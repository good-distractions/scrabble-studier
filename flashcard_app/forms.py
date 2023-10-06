# https://dev.to/earthcomfy/creating-the-sign-up-page-part-ii-5a3a
from django import forms

FILTER_CHOICES = [
    ("all", "All Words"),
    ("q_no_u", "With Q not U"),
    # ("palindrome","Palindromes"),
    # ("no_vowels","Words without Vowels"),
    # ("7l5v","7 letter words with 5 or more vowels"),
    # ("5l4v","5 letter words with 4 vowels"),
    # ("satine","7 letter words containing s-a-t-i-n-e"),
    # ("endinz","End in Z"),
    # ("length","Filter by Length Only"),
    # ("xlcontainy","Filter by Character & Length"),
    # ("contain_xyz","Filter by Character Only"),
]

class CustomFilterForm(forms.Form):
    filter_type = forms.ChoiceField(widget=forms.Select, choices=FILTER_CHOICES)
    substring = forms.CharField(widget=forms.TextInput(),max_length=30)
    word_length = forms.IntegerField(widget=forms.NumberInput(),min_value=1)
    
    def __init__(self, *args, **kwargs):
        super(CustomFilterForm, self).__init__(*args, **kwargs)
        self.fields['substring'].required = False
        self.fields['word_length'].required = False
    
    def load_data(self):
        # do something with self.cleaned_data
        pass