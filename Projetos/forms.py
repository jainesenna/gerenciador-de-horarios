from django import forms

class NameForm(forms.Form):
    materia = forms.CharField(label='materia', max_length=100)
    conteudo = forms.CharField(label='conteudo', max_length=255)