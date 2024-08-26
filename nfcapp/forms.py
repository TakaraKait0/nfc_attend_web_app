from django import forms


class RegistrationForm(forms.Form):
    name = forms.CharField(label='名前', max_length=100)
    grade = forms.CharField(label='学年', max_length=10)
