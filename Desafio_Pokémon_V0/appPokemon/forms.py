from django import forms


class CityForm(forms.Form):
    """docstring for CityForm"""
    cidade = forms.CharField(max_length=100)
