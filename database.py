import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='thrive',
        user='root',
        password='password'
    )