from server import mysql_connection


cursor = mysql_connection.cursor()
cursor.execute('SELECT * FROM users')
users1 = cursor.fetchall()
print(users1)