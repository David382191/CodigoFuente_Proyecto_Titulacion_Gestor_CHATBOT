######################################################################################
######################################################################################
import psycopg2
from psycopg2 import Error

def get_db():
    try:
        connection = psycopg2.connect(
            host="dpg-d5sm0dc9c44c739csnhg-a.oregon-postgres.render.com",
            port="5432",
            user="admin",
            password="x9Hw2ZP0vV0LN74kWwSXufApbqhbO2nO",
            dbname="chatbot_db_z5tb",
            sslmode="require"   # 🔑 ESTA LÍNEA
        )
        return connection

    except Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None
######################################################################################
######################################################################################