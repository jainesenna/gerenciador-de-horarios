# povoandoSqlite.py
import sqlite3

conn = sqlite3.connect('trabalhobd2019_2')
cursor = conn.cursor()

# criando uma lista de dados
usuarios = [ ("Pedro", "pedrojonassm@gmail.com", "pedrojonas13"),
    ("Jaine", "jainesantossenna191@gmail.com", "jaine123")
]

materias = [("23T34", "Arquitetura"), ("45T56", "Banco de Dados"), 
    ("46T34", "Engenharia de Software"),("24T12", "Inglês Técnico"), 
    ("46M45","Matematica Financeira"), ("5T34 6T12", "Programação Web")

]

grade = [
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)
]

atividades = [
    (1, 3, "teste")
]

horaestudo = [
    (1, 1, "2M12"), (1,4,"2M34"), (1,2,"4M12"), 
    (1,5,"4M34"), (1,3,"4M56"), (1,6,"5M12")
]
# inserindo dados na tabela
cursor.executemany("""
INSERT INTO usuario(nome, email, senha)
VALUES (?,?,?)
""", usuarios)

cursor.executemany("""
INSERT INTO materia (horario, nome)
VALUES (?,?)
""", materias)

cursor.executemany("""
INSERT INTO gradeestudo (aluno, materias)
VALUES (?,?)
""", grade)

cursor.executemany("""
INSERT INTO atividade(aluno, materia, conteudo)
VALUES (?,?,?)
""", atividades)

cursor.executemany("""
INSERT INTO horarioestudo (aluno, materias, horario)
VALUES (?,?,?)
""", horaestudo)

conn.commit()

print('Dados inseridos com sucesso.\n\n')

'''# lendo os dados
cursor.execute("""
SELECT * FROM dbteste;
""")

for linha in cursor.fetchall():
    print(linha)
    '''

conn.close()




