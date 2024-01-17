from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)

# SQLAlchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://db_user:db_password@mysql_db:3306/my_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# check if the connection is successfully established or not
with app.app_context():
    try:
        # db.session.execute('SELECT 1')
        db.session.execute(text('SELECT 1'))
        print('\n\n----------- Connection successful!')
    except Exception as e:
        print('\n\n----------- Connection failed ! ERROR : ', e)

app.config['SECRET_KEY'] = 'secret'

bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
from web import routes