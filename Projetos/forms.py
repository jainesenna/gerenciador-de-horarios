from django import forms

class atividades_form(forms.Form):
    materia = forms.CharField(label='materia', max_length=100, required=False)
    conteudo = forms.CharField(label='conteudo', max_length=255, required=False)

class horarios_form(forms.Form):
    id = forms.IntegerField(label = 'id')
    horario = forms.CharField(label='horario', max_length=255)
    materia = forms.CharField(label='materia', max_length=100)