import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database = 'Pong'
)

cursor = conexao.cursor()

# cursor.execute("create database Pong")

# cursor.execute('CREATE TABLE jogo (id_jogo int(3) AUTO_INCREMENT PRIMARY KEY, tempo float(6), vencedor varchar(2))')


cursor.execute('SELECT * FROM jogo')
for partida in cursor:
    print(partida)


conexao.close()
