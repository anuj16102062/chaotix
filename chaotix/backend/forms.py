from django import forms

class ImageGenerationForm(forms.Form):
    text1 = forms.CharField(label='Promt 1', max_length=100)
    text2 = forms.CharField(label='Promt 2', max_length=100)
    text3 = forms.CharField(label='Promt 3', max_length=100)
