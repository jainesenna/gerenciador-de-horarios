from Projetos.models import Materia, Usuario, Atividade, Gradeestudo, Horarioestudo
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

usuario = Usuario.objects.get(id=1)

def Principal(request):
    estudos = Horarioestudo.objects.filter(aluno = usuario).values_list('materias', 'horario')
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    return render(request, 'Projetos/principal.html', locals())

def horarios_auto(request):
    estudos = Horarioestudo.objects.filter(aluno = usuario)
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    sla = ''
    k = 0
    materias_sem_h = Materia.objects.exclude(id__in=Horarioestudo.objects.filter(aluno=usuario).values_list('materias'))
    for x in ['2','3','4','5','6','7']:
       dia = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias'), horario__startswith = x).order_by('horario') # separando as matérias por dia
       if len(dia) > 0 and dia[k] in materias_sem_h: #verifica se
           print("X:" + x + "\n")
           for y in ["12","34","56"]:
               if len(Horarioestudo.objects.filter(aluno=usuario, horario = x+"M"+y)) == 0: #verifica se ja não existe nada naquele horário
                   q = Horarioestudo(aluno=usuario, materias=dia[k], horario = x+"M"+y) # criando novo horário de estudo
                   q.save()
                   print("Salvo: " + usuario.nome +"  "+ dia[k].nome +"  "+ "horario:  "+x+"M"+y)
                   k+=1
               if k>len(dia)-1:
                   k = 0
                   break
    return render(request, 'Projetos/principal.html', locals())

def horarios_manual(request):
    estudos = Horarioestudo.objects.filter(aluno = usuario).values_list('materias', 'horario')
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    return render(request, 'Projetos/principal.html', locals())

def apagar_horarios(request):
    estudos = Horarioestudo.objects.filter(aluno = usuario)
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    Principal(request)
    for x in estudos:
        x.delete()
    Principal(request)
    return render(request, 'Projetos/principal.html', locals())

