import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Senha padrão do XAMPP é vazia
        database="estudio_tatuagem"
    )