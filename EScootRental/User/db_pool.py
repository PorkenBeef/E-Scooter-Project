import mysql.connector
from mysql.connector import pooling

db_config = {
    "user": "root",
    "password": "maamo5",
    "host": "127.0.0.1",
    "database": "EScoot",
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=30,
    **db_config
)

def get_connection():
    return connection_pool.get_connection()

def query_database(query, params=None):
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
