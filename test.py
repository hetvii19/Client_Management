import mysql.connector

# MySQL Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "client_management"
}

def test_connection():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print(tables)
    connection.close()

test_connection()
