import mysql.connector
from MYSQL_CONNECTION_POOLING.python.db_pool import get_connection

def query_database(query, params=None):
    try:
        # Get a connection from the pool
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Execute the query
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Ensure the connection is returned to the pool
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    sql_query = "SELECT * FROM adminacc WHERE password = %s"
    params = ("value",)
    results = query_database(sql_query, params)
    print(results)
