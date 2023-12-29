from web import mysql_connection

class Database():

    def get_users():
        cursor = mysql_connection.cursor()
        cursor.execute('SELECT * FROM users')
        return cursor.fetchall()
