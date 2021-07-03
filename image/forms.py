
from django import forms

class Upload(forms.Form):
    object = forms.ImageField(required = True)
    config = forms.FloatField(required = True, max_value = 1, min_value = 0)
    model = forms.CharField(widget = forms.HiddenInput(), required = True)
