from django import forms
from accounts.models import Condition, Experiment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import get_user_model
from accounts.models import Researcher
# define choices for the game type dropdown
GAME_CHOICES = [("MT", "Map Task"),
                ("PD", "Prisoner's Dilemma"),
                ("TG", "Trust Game")]

class ResearcherRegisterForm(UserCreationForm):
    """ A form to register a new researcher. Inherits from Django's UserCreationForm. """
    class Meta:
        model = User
        # specify the fields to include in the form
        fields = ('first_name', 'last_name','username','email','password1','password2')
        widgets = {
            # add a css class to each form field for styling
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_username(self):
        """Check if the chosen username is unique, and raise an error if not."""
        user_model = get_user_model()
        username = self.cleaned_data['username']
        try:
            user_model.objects.get(username__iexact=username)
        except user_model.DoesNotExist:
            return username
        raise forms.ValidationError(("This username already exists"))
    
    def __init__(self, *args, **kwargs):
        super(ResearcherRegisterForm, self).__init__(*args, **kwargs)

        for _, field in self.fields.items():
            if field in self.errors:
                field.widget.attrs.update({
                    'autofocus': ''
                })

                break

class ExperimentForm(forms.ModelForm):
    """A form to create a new experiment."""
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
    
    def __init__(self, *args, **kwargs):
        """ Store the value of request so we can access the currently logged in user in validation."""
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_experiment_name(self):
        experiment_name = self.cleaned_data['experiment_name']
        try:
            current_researcher = Researcher.objects.get(userkey=self.request.user)
            Experiment.objects.get(created_by = current_researcher, name = experiment_name)
        except Experiment.DoesNotExist:
            return experiment_name
        raise forms.ValidationError(("This experiment name already exists"))

class GameConditions(forms.ModelForm):
    """ This form is used to create and edit game conditions."""
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
    
    def __init__(self, *args, **kwargs):
        """ Store value of request so we can access the currently logged in user in validation. """
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        if self.request.user:
            self.fields['experiment'].queryset = Experiment.objects.filter(created_by = Researcher.objects.get(userkey = self.request.user))

    def clean_condition_name(self):
        """ This function validates the condition name. """
        condition_name = self.cleaned_data['condition_name']
        try:
            current_researcher = Researcher.objects.get(userkey=self.request.user)
            Condition.objects.get(created_by = current_researcher, name = condition_name)
        except Condition.DoesNotExist:
            return condition_name
        raise forms.ValidationError(("This condition name already exists"))
    
    def clean_amount_of_items(self):
        """ This function validates the amount of items. """
        amount_of_items = self.cleaned_data['amount_of_items']
        if amount_of_items < 0:
            raise forms.ValidationError(("You cannot set negative items"))
        elif amount_of_items == 0:
            raise forms.ValidationError(("You must set at least one item"))
        else:
            return amount_of_items



class ChooseGame(forms.Form):
    """ This form is used to choose a game type. """
    game_choice = forms.ChoiceField(
        choices=GAME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mb-3'})
    )
