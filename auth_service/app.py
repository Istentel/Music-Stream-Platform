from flask import Flask, jsonify, request, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from  werkzeug.security import generate_password_hash, check_password_hash
import os, jwt, datetime
from functools import wraps
from jwt.exceptions import InvalidTokenError
from flask_cors import CORS

app = Flask(__name__)

CORS(app, origins=['http://localhost:8080'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'user'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql_db'),
    os.getenv('DB_NAME', 'db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    email  = db.Column(db.String(100), unique=True, nullable=False)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, text_password):
        self.password_hash = bcrypt.generate_password_hash(text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}: {self.email}>'
    

class Favourite(db.Model):
    __tablename__ = 'favourite'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    song_id = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', backref=db.backref('favourites', lazy=True))

# Create table
with app.app_context():
    db.create_all()

def createJWT(email, secret):
    return jwt.encode(
        {
            "email": email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(datetime.timezone.utc),
        },
        secret,
        algorithm="HS256",
    )

@app.route('/api/hello', methods=['GET'])
def get_hello():
    return jsonify({'message': 'Hello from the db_gateway server!'})

@app.route('/favourites/add', methods=['POST'])
def add_favourite():
    data = request.json
    email = data.get('email')
    song_id = data.get('song_id')

    if not email or not song_id:
        return jsonify({'message': 'Email and song ID are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Check if the song is already a favorite for the user
    if Favourite.query.filter_by(user_id=user.id, song_id=song_id).first():
        return jsonify({'message': 'Song already a favorite'}), 400

    # Create a new favorite entry
    favourite = Favourite(user_id=user.id, song_id=song_id)
    db.session.add(favourite)
    db.session.commit()

    return jsonify({'message': 'Favorite song added successfully'}), 200

@app.route('/favourites/remove', methods=['POST'])
def remove_favourite():
    data = request.json
    email = data.get('email')
    song_id = data.get('song_id')

    if not email or not song_id:
        return jsonify({'message': 'Email and song ID are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    favourite = Favourite.query.filter_by(user_id=user.id, song_id=song_id).first()
    if not favourite:
        return jsonify({'message': 'Song is not a favorite for this user'}), 404

    # Remove the favorite entry
    db.session.delete(favourite)
    db.session.commit()

    return jsonify({'message': 'Favorite song removed successfully'}), 200

@app.route('/favourites/<string:email>', methods=['GET'])
def get_favourite_songs(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    favourites = Favourite.query.filter_by(user_id=user.id).all()
    song_ids = [f.song_id for f in favourites]
    return jsonify({'song_ids': song_ids}), 200

@app.route("/validate", methods=["POST"])
def validate_token():
    # Get the token from the request
    token = request.json.get('token')

    if not token:
        return jsonify({'message': 'Token is missing'}), 400

    try:
        # Verify and decode the token
        decoded_token = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=['HS256'])

        if 'exp' in decoded_token:
            current_time = datetime.datetime.now(datetime.timezone.utc)
            token_exp_time = datetime.datetime.utcfromtimestamp(decoded_token['exp']).replace(tzinfo=datetime.timezone.utc)
            if current_time > token_exp_time:
                return jsonify({'message': 'Token has expired'}), 401

        user_email = decoded_token['email']

        # Token is valid
        return jsonify({'email': user_email}), 200
    
    except InvalidTokenError:
        # Token is invalid or tampered with
        return jsonify({'message': 'Invalid token'}), 401

@app.route('/register', methods=['POST'])
def register_user():          
    # try:
    print("Call register api!")
    user = json.loads(request.json)

    first_name = user["firstname"]
    last_name = user["lastname"]
    new_password = user["password"]
    new_email = user["email"]

    if first_name and last_name and new_password and new_email and request.method == 'POST':
        new_user = User(firstname=first_name,
                        lastname=last_name, 
                        password=new_password,
                        email=new_email)
        
        db.session.add(new_user)
        db.session.commit()

        # generates the JWT Token
        token = createJWT(new_email, os.environ.get("JWT_SECRET"))

        return make_response(jsonify({'token' : token}), 201)
    else:
        return "No data available", 204
        
    # except Exception as e:
    #     return jsonify({'error': f"{e}"}), 500
    
@app.route('/login', methods=['GET'])
def login_user(): 
    auth = request.authorization

    if not auth:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
    
    attempted_user = User.query.filter_by(email=auth.username).first()
    
    if not attempted_user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
            )

    if attempted_user.check_password_correction(attempted_password=auth.password):
        # generates the JWT Token
        token = createJWT(attempted_user.email, os.environ.get("JWT_SECRET"))

        return make_response(jsonify({'token' : token}), 200)
    
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)