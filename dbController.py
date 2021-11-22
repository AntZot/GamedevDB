import mysql.connector
from mysql.connector import Error

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='azot'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    cursor = connection.cursor()
    cursor.execute("USE gamedev;")
    return connection

def CreateDatabase(dbConnection):
    with open('Resources/DataBase.sql') as f:
        with dbConnection.cursor() as cursor:
            cursor.execute(f.read(), multi=True)
        dbConnection.commit()
