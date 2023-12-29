from flask import Flask
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'mysql',
    'port': 3306,
    'database': 'db'
}

# Create a MySQL connection
mysql_connection = mysql.connector.connect(**db_config)

app.config['SECRET_KEY'] = 'secret'

from web import routes