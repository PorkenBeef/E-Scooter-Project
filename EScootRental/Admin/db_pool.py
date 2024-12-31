import mysql.connector
from mysql.connector import pooling

db_config = {
    "user": "root",
    "password": "maamo5",
    "host": "127.0.0.1",
    "database": "EScoot",
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="AdminPool",
    pool_size=5,
    **db_config
)

def get_connection():
    return connection_pool.get_connection()