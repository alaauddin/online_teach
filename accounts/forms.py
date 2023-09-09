from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator



class SignUpForm (UserCreationForm):
   

    
    email = forms.CharField(max_length=255, required=True, widget=forms.EmailInput())
    department = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model=User
        fields = {'first_name','last_name','username','email','department','phone_number', 'password1', 'password2'}