from django import forms
from atm_app.models import Card

class LoginForm(forms.Form):
    number = forms.CharField(
        max_length=16,
        min_length=16,
    )
#        widget=forms.HiddenInput(attrs={'id': "input_id"})