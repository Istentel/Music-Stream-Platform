from web import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(120), unique=False, nullable=False)
    lastname = db.Column(db.String(120), unique=False, nullable=False)
    email  = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}: {self.email}>'