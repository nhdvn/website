from django import forms

class Upload(forms.Form):
    imageField = forms.ImageField(required = True)
    imageConfig = forms.FloatField(required = True, max_value = 1, min_value = 0)
