from django import forms

class ValorationForm(forms.Form):
    rating = forms.RadioSelect()
    experience = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'input'
    }))