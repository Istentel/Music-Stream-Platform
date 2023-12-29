from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Set up SQLAlchemy with your Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import routes