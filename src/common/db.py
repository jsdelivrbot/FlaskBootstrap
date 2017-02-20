from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))
    first = db.Column(db.String(255))
    last = db.Column(db.String(255))

    def __init__(self, email, password, first, last):
        self.email = email
        self.password = bcrypt.hashpw(password.encode('UTF_8'),
                                      bcrypt.gensalt())
        self.first = first
        self.last = last

    def compare_pass(self, new_password):
        return bcrypt.checkpw(new_password.encode('UTF_8'),
                              self.password.encode('UTF_8'))

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(
        'User',
        backref=db.backref('posts', lazy='dynamic'))
    created = db.Column(db.DateTime)
    pub_date = db.Column(db.DateTime)
    title = db.Column(db.String(120), unique=True)
    body = db.Column(db.Text)

    def __init__(self, title, body, author, pub_date=None):
        self.title = title
        self.body = body
        self.created = datetime.utcnow()
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.author = author

    def __repr__(self):
        return '<Post %r>' % self.title
