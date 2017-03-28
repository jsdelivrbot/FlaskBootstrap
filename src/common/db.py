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
    excerpt = db.Column(db.String(500))

    def __init__(self, title, excerpt, body, author, pub_date=None):
        self.title = title
        self.body = body
        self.created = datetime.utcnow()
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.author = author
        self.excerpt = excerpt

    def __repr__(self):
        return '<Post %r>' % self.title

    def update(self, title, excerpt, body, pub_date):
        self.title = title
        self.body = body
        self.excerpt = excerpt
        self.pub_date = pub_date


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(
        'User',
        backref=db.backref('projects', lazy='dynamic'))
    created = db.Column(db.DateTime)
    pub_date = db.Column(db.DateTime)
    title = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text)
    excerpt = db.Column(db.String(500))
    thumbnail_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    thumbnail = db.relationship(
        'Image',
        backref=db.backref('images', lazy='dynamic'))

    images = db.relationship("ProjectImages")

    def __init__(self, title, excerpt, description, author, image,
                 pub_date=None):
        self.title = title
        self.description = description
        self.created = datetime.utcnow()
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.author = author
        self.excerpt = excerpt
        self.thumbnail = image

    def __repr__(self):
        return '<Project %r>' % self.title

    def update(self, title, excerpt, body, pub_date, thumbnail=None):
        self.title = title
        self.body = body
        self.excerpt = excerpt
        self.pub_date = pub_date
        if thumbnail is not None:
            self.thumbnail = thumbnail


class ProjectImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    image = db.relationship(
        'Image',
        backref=db.backref('project_images', lazy='dynamic',
                           cascade="all, delete-orphan"))

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self, project, image):
        self.image = image
        self.project_id = project.id


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    caption = db.Column(db.String(120))
    path = db.Column(db.String(1000))

    def __init__(self, caption, path):
        self.created = datetime.utcnow()
        self.caption = caption
        self.path = path

    def __repr__(self):
        return "<Image %s>" % self.caption
