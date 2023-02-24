from django import forms
from accounts.models import Condition

# bad but we can make a model to store each game later
GAME_CHOICES =[
    ("MG", "Map Game"),
]

class GameConditions(forms.ModelForm):
    amount_of_items = forms.IntegerField()
    restriction = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Condition
        fields = ('game_type','active')


    """"
    This is in case we want another model so that researchers can create
    their own game types (instead of us having to create and add them)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['game_type'].queryset = GameType.objects.all()"""

class ChooseGame(forms.Form):
    game_choice = forms.ChoiceField(choices = GAME_CHOICES)
