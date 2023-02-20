from django import forms
  
# creating a form 
class create_conditions(forms.Form):
    amount_items = forms.IntegerField()
    restriction = forms.CharField()