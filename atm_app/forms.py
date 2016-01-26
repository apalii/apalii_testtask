from django import forms
from atm_app.models import Card

class LoginForm(forms.Form):

    number = forms.CharField(
        max_length=19,
        min_length=19,
    )
    password = forms.IntegerField(
        min_value=0000,
        max_value=9999
    )
