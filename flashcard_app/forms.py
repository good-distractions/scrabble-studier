# https://dev.to/earthcomfy/creating-the-sign-up-page-part-ii-5a3a
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

FILTER_CHOICES = [
    ("all", "All Words"),
    ("q_no_u", "With Q not U"),
    ("palindrome","Palindromes"),
    ("no_vowels","Words without Vowels"),
    ("7l5v","7 letter words with 5 or more vowels"),
    ("5l4v","5 letter words with 4 vowels"),
    ("satine","7 letter words containing s-a-t-i-n-e"),
    ("endinz","End in Z"),
]

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']


class CustomFilterForm(forms.Form):
    filter_type = forms.ChoiceField(widget=forms.Select, choices=FILTER_CHOICES)
    substring = forms.CharField(widget=forms.TextInput(),max_length=30)
    word_length = forms.IntegerField(widget=forms.NumberInput(),min_value=1)
    time_between_words = forms.IntegerField(widget=forms.NumberInput(),min_value=1, initial=3)
    
    def __init__(self, *args, **kwargs):
        super(CustomFilterForm, self).__init__(*args, **kwargs)
        self.fields['substring'].required = False
        self.fields['word_length'].required = False
        self.fields['filter_type'].required = True
        self.fields['time_between_words'].required = True
    
    def load_data(self):
        # do something with self.cleaned_data
        pass