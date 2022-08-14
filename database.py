from mysql.connector import connect


def get_db_connection():
    return connect(
        host='localhost',
        database='thrive',
        user='root',
        password='password'
    )


