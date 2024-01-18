from web import db, bcrypt, loginManager
from flask_login import UserMixin

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
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