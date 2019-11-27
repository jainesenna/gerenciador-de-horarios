from django.db import models

# Create your models here.



class Materia(models.Model):
    horario = models.CharField(max_length=22, blank=True, null=True)
    nome = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'materia'
    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuario'
    def __str__(self):
        return self.nome
    def __id__(self):
        return self.id

class Gradeestudo(models.Model):
    aluno = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='aluno', primary_key=True)
    materias = models.ForeignKey('Materia', models.DO_NOTHING, db_column='materias')

    class Meta:
        db_table = 'gradeestudo'
        unique_together = (('aluno', 'materias'),)

class Atividade(models.Model):
    aluno = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='aluno')
    materia = models.ForeignKey('Materia', models.DO_NOTHING, db_column='materia', blank=True, null=True)
    conteudo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'atividade'
    def __str__(self):
        return self.conteudo