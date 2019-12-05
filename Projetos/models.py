from django.db import models

# Create your models here.

# Exclude = Contrário de filter

# Materia.objects.filter(id__lte=2) | pega as materias com id <= 2
# Materia.objects.exclude(id__lte=2) | pega as materias cujo o id não é <= 2

# Para mais comandos veja o "Comandos_Django_BD.txt"

class Atividade(models.Model):
    aluno = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='aluno')
    materia = models.ForeignKey('Materia', models.DO_NOTHING, db_column='materia', blank=True, null=True)
    conteudo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atividade'


class Gradeestudo(models.Model):
    aluno = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='aluno')
    materias = models.ForeignKey('Materia', models.DO_NOTHING, db_column='materias')

    class Meta:
        managed = False
        db_table = 'gradeestudo'


class Horarioestudo(models.Model):
    aluno = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='aluno')
    materias = models.ForeignKey('Materia', models.DO_NOTHING, db_column='materias')
    horario = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horarioestudo'


class Materia(models.Model):
    horario = models.CharField(max_length=22, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materia'


class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'usuario'