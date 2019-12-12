from django import forms

class atividades_form(forms.Form):
    materia = forms.CharField(label='Disciplina', max_length=100, required=False)
    conteudo = forms.CharField(label='Matéria', max_length=255, required=False)

class horarios_form(forms.Form):
    id = forms.IntegerField(label = 'Id')
    horario = forms.CharField(label='Horário', max_length=255)
    materia = forms.CharField(label='Disciplina', max_length=100)