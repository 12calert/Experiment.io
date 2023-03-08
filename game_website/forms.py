from django import forms
from accounts.models import Condition, Experiment

# bad but we can make a model to store each game later
GAME_CHOICES = [("MG", "Map Game")]

class ResearcherRegisterForm(forms.Form):
    forename = forms.CharField(
        max_length = 50,
        required = True,
        widget=forms.TextInput(attrs={'class': 'form-control'})            
    )
    surname = forms.CharField(
        max_length = 50,
        required = True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length = 50,
        required = True,
        widget=forms.TextInput(attrs={'class': 'form-control'})            
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required = True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required = True
    )

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
