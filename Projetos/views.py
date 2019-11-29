from Projetos.models import Materia, Usuario, Atividade, Gradeestudo, Horarioestudo
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

def Principal(request):
    usuario = Usuario.objects.get(id=1)

    estudos = Horarioestudo.objects.filter(aluno = usuario).values_list('materias', 'horario')
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    atividades = Atividade.objects.filter(aluno=usuario).values_list('materia', 'conteudo')
    lista_atividades = []
    sla = [] #vai guardar o nome da materia e o conteudo da atividade, respectivamente
    lista_estudos = []
    for e in estudos:
        for m in materias:
            if(e[0] == m.id):
                    sla.append(m.nome)
                    sla.append(e[1])
                    lista_estudos.append(sla)
                    sla = []
    for x in atividades:
        a = x[0]
        c = Materia.objects.filter(id=a)
        if (len(c)>0):
            sla.append(c[0].nome)
            sla.append(x[1])
            lista_atividades.append(sla)
            sla = []
    return render(request, 'Projetos/principal.html', locals())

def horarios_auto(request):
    usuario = Usuario.objects.get(id=1)

    estudos = Horarioestudo.objects.filter(aluno = usuario)
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    sla = ''
    k = 0
    materias_sem_h = Materia.objects.exclude(id__in=Horarioestudo.objects.filter(aluno=usuario).values_list('materias'))
    for x in ['1','2','3','4','5','6']:
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
    usuario = Usuario.objects.get(id=1)
    estudos = Horarioestudo.objects.filter(aluno = usuario).values_list('materias', 'horario')
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    return render(request, 'Projetos/principal.html', locals())

def apagar_horarios(request):
    usuario = Usuario.objects.get(id=1)
    estudos = Horarioestudo.objects.filter(aluno = usuario)
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    for x in estudos:
        x.delete()
    return render(request, 'Projetos/principal.html', locals())

