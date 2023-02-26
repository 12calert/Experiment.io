from django import forms
from accounts.models import Condition

# bad but we can make a model to store each game later
GAME_CHOICES = [("MG", "Map Game")]

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

    class Meta:
        model = Condition
        fields = ('game_type', 'active')
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
