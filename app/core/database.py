import mysql.connector
import os
from dotenv import load_dotenv

class Database:

    load_dotenv()

    def conectar(self):

        return mysql.connector.connect(
            host =      os.getenv("DB_HOST"),
            port =      os.getenv("DB_PORT"),
            database =  os.getenv("DB_NAME"),
            user =      os.getenv("DB_USER"),
            password =  os.getenv("DB_PASSWORD")
        )
    def desconectar(self, cursor=None, conexao=None):
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()