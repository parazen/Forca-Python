import sqlite3
from sqlite3 import Error
import os

def conexao(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def criar_tabela(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS palavras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                palavra TEXT NOT NULL,
                tema TEXT NOT NULL
            )
        ''')
    except Error as e:
        print(e)

def inserir_palavra(conn , palavra, tema):
    palavras = [
        (palavra, tema)
    ]
    try:
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO palavras (palavra, tema)
            VALUES (?, ?)
        ''', palavras)
        conn.commit()
    except Error as e:
        print(e)

def obter_palavras(conn):
    """Retorna todas as palavras do banco de dados"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT palavra, tema FROM palavras')
        return cursor.fetchall()
    except Error as e:
        print(e)
        return None

def obter_palavra_aleatoria(conn):
    """Retorna uma palavra aleatória do banco de dados"""
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT palavra, tema FROM palavras ORDER BY RANDOM() LIMIT 1')
        return cursor.fetchone()
    except Error as e:
        print(e)
        return None

def main():
    database = "database/palavras.db"
    
    # Garante que a pasta database existe
    os.makedirs(os.path.dirname(database), exist_ok=True)
    
    conn = conexao(database)
    if conn is not None:
        criar_tabela(conn)
        
        # Verifica se a tabela está vazia
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM palavras")
        count = cursor.fetchone()[0]
        
        if count == 0:
            palavras_iniciais = [
                ("python", "linguagem"),
                ("gato", "animal"),
                ("cachorro", "animal"),
                ("carro", "transporte"),
                ("aviao", "transporte"),
                ("computador", "tecnologia"),
                ("celular", "tecnologia"),
                ("mesa", "moveis"),
                ("cadeira", "moveis"),
                ("livro", "educacao")
            ]
            cursor.executemany("INSERT INTO palavras (palavra, tema) VALUES (?, ?)", palavras_iniciais)
            conn.commit()
            print("Palavras iniciais inseridas.")
        conn.close()
        
if __name__ == '__main__':
    main()
