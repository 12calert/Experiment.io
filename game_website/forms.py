from django import forms
from accounts.models import Condition, Experiment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import get_user_model
# bad but we can make a model to store each game later
GAME_CHOICES = [("MG", "Map Game")]

class ResearcherRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','email','password1','password2')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
        }
    """ check to see if the username is unique and appropriate error"""
    def clean_username(self):
        user_model = get_user_model()
        username = self.cleaned_data['username']
        try:
            user_model.objects.get(username__iexact=username)
        except user_model.DoesNotExist:
            return username
        raise forms.ValidationError(("This username already exists"))

class ExperimentForm(forms.ModelForm):
    experiment_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control text-center', 'style': 'width: 300px; margin: auto;'}),
    )

    class Meta:
        model = Experiment
        fields = ('experiment_name', 'active',)
        widgets = {
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class GameConditions(forms.ModelForm):
    amount_of_items = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control text-center', 'style': 'width: 150px; margin: auto;'})
    )
    restriction = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control text-center', 'style': 'width: 150px; margin: auto;'})
    )
    condition_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control text-center', 'style': 'width: 150px; margin: auto;'})
    )
    game_type = forms.ChoiceField(
        choices=GAME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mb-3', 'style': 'width: 300px; margin: auto;'})
    )

    class Meta:
        model = Condition
        fields = ('game_type', 'active', 'experiment')
        widgets = {
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'active': 'Active'
        }



class ChooseGame(forms.Form):
    game_choice = forms.ChoiceField(
        choices=GAME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mb-3'})
    )
