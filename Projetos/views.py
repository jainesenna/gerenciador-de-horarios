from Projetos.models import Materia, Usuario, Atividade, Gradeestudo, Horarioestudo
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from .forms import atividades_form, horarios_form

def Principal(request):
    usuario = Usuario.objects.get(id=1)

    form = atividades_form(request.POST or None)

    if form.is_valid():
        m = form.cleaned_data
        mm = Materia.objects.filter(nome = m["materia"])
        cc = m["conteudo"]
        Atividade(aluno = usuario, conteudo = cc, materia = mm[0]).save()

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
    try:
        choice = request.GET["escolha"] # estudar ou revisar. retorna o id das opções cujo nome é "escolha"
    except:
        choice = ""
    estudos = Horarioestudo.objects.filter(aluno = usuario)
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    sla = ''
    k = 0
    materias_sem_h = Materia.objects.exclude(id__in=Horarioestudo.objects.filter(aluno=usuario).values_list('materias'))
    if choice == "estudar":
        for x in ['1','2','3','4','5','6']:
            dia = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias'), horario__startswith = x).order_by('horario') # separando as matérias por dia
            if len(dia) > 0 and dia[k] in materias_sem_h: #verifica se
                print("X:" + x + "\n")
                for y in ["12","34","56"]:
                    if len(Horarioestudo.objects.filter(aluno=usuario, horario = x+"M"+y)) == 0: #verifica se ja não existe nada naquele horário
                        q = Horarioestudo(aluno=usuario, materias=dia[k], horario = x+"M"+y) # criando novo horário de estudo
                        q.save()
                        k+=1
                    if k>len(dia)-1:
                        k = 0
                        break
    elif choice == "revisar":
        for x in ['1','2','3','4','5','6']:
            dia = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias'), horario__startswith = x).order_by('horario') # separando as matérias por dia
            if len(dia) > 0 and dia[k] in materias_sem_h: #verifica se
                for y in ["12","34","56"]:
                    if len(Horarioestudo.objects.filter(aluno=usuario, horario = str(int(x)+1)+"M"+y)) == 0: #verifica se ja não existe nada naquele horário
                        q = Horarioestudo(aluno=usuario, materias=dia[k], horario = str(int(x)+1)+"M"+y) # criando novo horário de estudo
                        q.save()
                        k+=1
                    if k>len(dia)-1:
                        k = 0
                        break
    else:
        erro = "Você não fez uma escolha"
    return Principal(request)

def horarios_manual(request):
    usuario = Usuario.objects.get(id=1)
    estudos = Horarioestudo.objects.filter(aluno = usuario).values_list('id', 'materias', 'horario').order_by('horario')
    lista_estudos = []
    sla = []
    erro = ""
    for e in estudos:
        m = Materia.objects.filter(id=e[1])
        sla.append(e[0])
        sla.append(m[0].nome)
        sla.append(e[2])
        lista_estudos.append(sla)# sla = [id do horario de estudo, nome da materia que esta estudando, horario da materia]
        sla=[]

    try:
        apagar = request.POST.getlist("apagar")
    except:
        apagar = []
        erro = "Não deu certo"
    if len(apagar) > 0:
        for x in apagar:
            Horarioestudo.objects.filter(aluno=usuario, id=int(x)).delete()
    form = horarios_form(request.POST or None)
    
    if form.is_valid():
        m = form.cleaned_data
        ida = m['id']
        hh = m['horario']
        if len(Horarioestudo.objects.filter(id=ida, aluno=usuario)) > 0: # editando o horario de uma materia
            h = Horarioestudo.objects.get(id=ida, aluno = usuario)
            if len(hh) != 4 and len(hh) != 9 and len(hh) != 0:
                erro = "o horario preenchido não tem 4 ou 9 caracteres"
            else:
                if len(Materia.objects.filter(nome = m['materia'], id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias'))) > 0: #se mandar nulo, o index range é menor que 0:
                    mm = Materia.objects.filter(nome = m['materia'], id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')) # recebe a nova materia
                else:
                    mm = Materia.objects.filter(id=h.materias.id, id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')) # recebe a materia que ja estava lá

                h.delete()
                h.horario = hh
                h.id = ida
                h.save()

        else: #criando um novo horario de estudo
            # {'id': 1, 'horario': '1M12', 'materia': 'Inglês Técnico'}
            if len(Horarioestudo.objects.filter(horario=hh, aluno = usuario)) > 0: # verifica se o horario de estudo está preenchido
                erro = "horario já preenchido"
            elif len(hh) != 4 and len(hh) != 9:
                erro = "o horario preenchido não tem 4 caracteres"
            else:
                mm = Materia.objects.filter(nome = m['materia'], id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias'))
                if (len(mm) > 0):
                    if (len(hh) == 4):
                        if len(Horarioestudo.objects.filter(horario=hh, aluno = usuario)) > 0:
                            erro = "Horário já ocupado"
                        else:
                            Horarioestudo(aluno = usuario, materias=mm[0], horario = hh).save()
                    elif (len(hh) == 9):
                        #str = 1M12 2M12
                        a = hh[:4] #1M12
                        b = hh[5:] #2M12
                        if len(Horarioestudo.objects.filter(horario__contains=a, aluno = usuario)) > 0 or len(Horarioestudo.objects.filter(horario__contains=b, aluno = usuario)) > 0:
                            erro = "Horario ja ocupado"
                        else:
                            Horarioestudo(aluno = usuario, materias=mm[0], horario = hh).save()
                else:
                    erro = "Você não esta cadastrado nessa matéria"
    
    return render(request, 'Projetos/horarios.html', locals())

def apagar_horarios(request):
    usuario = Usuario.objects.get(id=1)
    estudos = Horarioestudo.objects.filter(aluno = usuario)
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    for x in estudos:
        x.delete()
    return Principal(request)

def editar_atividades(request):
    lista_atividades = []
    sla = []
    form = atividades_form(request.POST or None)
    usuario = Usuario.objects.get(id=1)
    materias = Materia.objects.filter(id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias')).order_by('horario')
    atividades = Atividade.objects.filter(aluno=usuario).values_list('materia', 'conteudo', 'id')
    erro = ""

    try:
        apagar = request.POST.getlist("apagar")
    except:
        apagar = []
        erro = "Não deu certo"
    if len(apagar) > 0:
        for x in apagar:
            Atividade.objects.filter(aluno=usuario, id=int(x)).delete()
    else:
        try:
            choice = request.POST["escolha"] # estudar ou revisar. retorna o id das opções cujo nome é "escolha"
            # Aqui foi usado post por causa no templat, que no form está descrito que o method é um post
        except:
            choice = ""

        if choice == "apagar_tudo":
            for x in Atividade.objects.filter(aluno=usuario):
                x.delete()
        elif form.is_valid():
            m = form.cleaned_data
            cc = m["conteudo"]
            mm = Materia.objects.filter(nome = m["materia"], id__in=Gradeestudo.objects.filter(aluno=usuario).values_list('materias'))
            if choice == "apagar_materia":
                for x in Atividade.objects.filter(materia=mm[0],aluno=usuario):
                    x.delete()
            else:
                if cc != "":
                    Atividade(materia=mm[0], conteudo=cc, aluno = usuario).save()
        
    for x in atividades:
        a = x[0]
        c = Materia.objects.filter(id=a)
        if (len(c)>0):
            sla.append(c[0].nome) # matéria
            sla.append(x[1]) #conteúdo
            sla.append(str(x[2])); #id
            lista_atividades.append(sla)
            sla = []

    return render(request, 'Projetos/atividades.html', locals())