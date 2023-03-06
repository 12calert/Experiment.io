from django.contrib.auth.models import User 
from accounts.models import Game
from django import forms

class RegisterForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    surname = forms.CharField(max_length=50)
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password"]

 
    