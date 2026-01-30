######################################################################################
######################################################################################
import mysql.connector
from mysql.connector import Error

def get_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",        # o IP / dominio
            port=3306,
            user="root",
            password="12345",
            database="chatbot_secretaria",
            ssl_disabled=True        # MySQL local normalmente sin SSL
        )
        return connection

    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

######################################################################################
#####################################################################################