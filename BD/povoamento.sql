
#use trabalhobd2019_2;
insert into usuario(nome, email, senha) values ("Pedro", "pedrojonassm@gmail.com", "pedrojonas13");

insert into materia (horario, nome) values ("23T34", "Arquitetura"), ("45T56", "Banco de Dados"), ("46T34", "Engenharia de Software"),
("24T12", "Inglês Técnico"), ("46M45","Matematica Financeira"), ("5T34 6T12", "Programação Web");

insert into gradeEstudo (aluno, materias) values (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6);

insert into atividade(aluno, materia, conteudo) values (1, 3, "teste");

insert into HorarioEstudo (aluno, materias, horario) values (1, 1, "3M12");

# pegando as materias que um aluno esta dentro || Para a página de aluno
select materia.nome from usuario, materia, gradeEstudo where gradeEstudo.materias = materia.id and usuario.id = gradeEstudo.aluno and usuario.nome = "Pedro";

# pegando os alunos que estão dentro de uma materia || para a página de matéria:
select usuario.nome from usuario, materia, gradeEstudo where gradeEstudo.materias = materia.id and usuario.id = gradeEstudo.aluno and materia.nome = "Arquitetura";

# Pegando todas as matérias || pesquisa de matéria
select distinct materia.nome from materia;

# Pegando todos os alunos || pesquisa de aluno
select distinct usuario.nome from usuario;

#pegando as atividades cadastradas pelo aluno X || Atividades
select materia.nome, atividade.conteudo from atividade, usuario, materia where materia.id = atividade.materia and atividade.aluno = usuario.id and usuario.nome="Pedro";

# Pegando os horários de estudo de um usuario
select u.nome, m.nome, h.horario from usuario u, materia m, HorarioEstudo h, gradeEstudo g where g.aluno = u.id and g.materias = m.id and h.aluno = u.id and h.materias = m.id;

