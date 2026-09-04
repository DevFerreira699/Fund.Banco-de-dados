import sqlite3

conexao = sqlite3.connect ("banco.db")
cursor = conexao.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, idade INTEGER)")


cursor.execute("INSERT INTO usuarios (nome, idade) VALUES (?, ?)", ("João", 25))
cursor.execute("INSERT INTO usuarios (nome, idade) VALUES (?, ?)", ("Maria", 30))
conexao.commit()

cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()

print("Usuários cadastrados:")
for usuario in usuarios:
    print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Idade: {usuario[2]}") 

conexao.close()
