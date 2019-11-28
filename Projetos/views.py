from Projetos.models import Materia, Usuario, Atividade, Gradeestudo, Horarioestudo
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render
from django import forms
from .forms import UserForm


def Principal(request):
    sla = 'a'
    try:
        sla = request.POST['editar']
    except (KeyError):
        # Redisplay the question voting form.
        print("erro")
    usuario = Usuario.objects.get(id=1)
    estudos = Horarioestudo.objects.filter(aluno = usuario)
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    if sla == "automatico":
        k = 0
        for x in ['2','3','4','5','6','7']:
            dia = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias'), horario__startswith = x).order_by('horario') # separando as matérias por dia
            if len(dia) > 0:
                print("X:" + x + "\n")
                for y in ["12","34","56"]:
                    print(y)
                    if len(Horarioestudo.objects.filter(aluno=usuario, horario = x+"M"+y)) == 0: #verifica se ja não existe nada naquele horário
                        q = Horarioestudo(aluno=usuario, materias=dia[k], horario = x+"M"+y) # criando novo horário de estudo
                        q.save()
                        print("Salvo: " + usuario.nome +"  "+ dia[k].nome +"  "+ "horario:  "+x+"M"+y)
                        k+=1
                    if k>len(dia)-1:
                        k = 0
                        break

    elif (sla == "apagar"):
        for x in estudos:
            x.delete()
    return render(request, 'Projetos/principal.html', locals())