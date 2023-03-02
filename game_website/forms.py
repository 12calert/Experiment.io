from django import forms
from accounts.models import Condition, Experiment

# bad but we can make a model to store each game later
GAME_CHOICES = [("MG", "Map Game")]

class ExperimentForm(forms.Form):
    experiment_name = forms.CharField(
        max_length = 50,
        required = True,
        widget = forms.TextInput(
            attrs = {
            'class': 'form-control',
            'placeholder': 'Enter a name for the experiment',
            'style': 'width 500px; margin: auto;'
            }
        )
    )
    active = forms.BooleanField(
        required = True,
        widget = forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'id': 'active'
            }
        )
    )

class GameConditions(forms.ModelForm):
    amount_of_items = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount of items',
                'style': 'width: 200px; margin: auto;'
            }
        )
    )
    restriction = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter any special restrictions (optional)',
                'style': 'width: 500px; margin: auto;'
            }
        )
    )
    condition_name = forms.CharField(
        max_length = 50,
        required = True,
        widget = forms.TextInput(
        attrs = {
        'class': 'form-control',
        'placeholder': 'Enter a name for the condition',
        'style': 'width 500px; margin: auto;'
        }
        )
    )

    class Meta:
        model = Condition
        # need to change experiment widget styles
        fields = ('game_type', 'active','experiment')
        widgets = {
            'game_type': forms.Select(
                attrs={
                    'class': 'form-select mb-3',
                    'aria-label': 'Select game type',
                    'style': 'width: 200px; margin: 0 auto; display: block;'
                }
            ),
            'active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'id': 'active'
                }
            )
        }

        labels = {
            'active': 'Active'
        }

class ChooseGame(forms.Form):
    game_choice = forms.ChoiceField(
        choices=GAME_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select mb-3',
                'aria-label': 'Select game'
            }
        )
    )
