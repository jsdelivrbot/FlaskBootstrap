from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    first = db.Column(db.String(255))
    last = db.Column(db.String(255))

    def __init__(self, email, password, first, last):
        self.email = email
        self.password = bcrypt.hashpw(password.encode('UTF_8'), bcrypt.gensalt())
        self.first = first
        self.last = last

    def compare_pass(self, new_password):
        return bcrypt.checkpw(new_password.encode('UTF_8'), self.password.encode('UTF_8'))

    def __repr__(self):
        return '<User %r>' % self.username



