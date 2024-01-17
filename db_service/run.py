import os, requests
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_DATABASE_USER"] = os.environ.get("MYSQL_USER")
app.config["MYSQL_DATABASE_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
app.config["MYSQL_DATABASE_DB"] = os.environ.get("MYSQL_DB")
app.config["MYSQL_DATABASE_HOST"] = os.environ.get("MYSQL_HOST")
app.config["MYSQL_PORT"]= os.environ.get("MYSQL_PORT")

mysql = MySQL()
#mysql.init_app(app)

@app.route('/users', methods=['GET'])
def get_users():
    print('Got here!\n')
    try:
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM users")
        users_data = cur.fetchall()
        cur.close()
        if(users_data):
            return jsonify({'users': users_data})
        else:
            return jsonify({'users': "no users found!"})
    except Exception as e:
        return jsonify({'error': f"{e}"})
    


@app.route('/users', methods=['POST'])
def register_user():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    password_hash = request.json['password_hash']
    email = request.json['email']

    cur = mysql.get_db().cursor()
    query = f"INSERT INTO users(firstname, lastname, password_hash, email) VALUES('{firstname}', '{lastname}', '{password_hash}', '{email}')"
    cur.execute(query)
    cur.close()

if __name__ == "__main__":
    cur = mysql.get_db().cursor()
    query = """CREATE TABLE IF NOT EXISTS users(
    id int not null AUTO_INCREMENT,
    firstname varchar(50) NOT NULL,
    lastname varchar(50) NOT NULL,
    password_hash varchar(60) NOT NULL,
    email varchar(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
    );"""
    cur.execute(query)

    query_users = """INSERT INTO users(firstname, lastname, password_hash, email)
VALUES("Cristian", "Alexandru", "pass", "cristi@yahoo.com"), ("test", "test2", "pasdf" "test@yahoo.com")"""
    cur.execute(query_users)

    app.run(host="0.0.0.0", port=5000)

# connection = mysql.connector.connect(
#     user='root',
#     password='root',
#     host='mysql',
#     port="3306",
#     database='db'
# )

# print("DB connected!")

# cursor = connection.cursor()
# cursor.execute('SELECT * FROM users')
# users = cursor.fetchall()
# connection.close()

# print(users)