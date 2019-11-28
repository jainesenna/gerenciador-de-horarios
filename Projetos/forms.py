from django import forms

class opcao(forms.Form):
    escolha = forms.CharField(label='sla', max_length=100)