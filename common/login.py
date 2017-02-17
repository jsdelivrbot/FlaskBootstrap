from functools import wraps
from flask import g, request, redirect, url_for


class AuthException(Exception):
    pass


@login_manager.user_loader
def load_user(user_id):
        return User.get(user_id)


class UserLogin(object):
    def __init__(self):
        self.uid = None

    def login(self, email, password):
        user = User.query.filter_by(email=postdata["email"]).one()
        if not user.compare_pass(postdata["password"]):
            raise AuthException("Invalid username or password")
        self.uid = user.id
        self.email = user.email
        self.first = first
        self.last = last

    def is_authenticated(self):
        return self.uid is not None 

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return self.uid is None

    def get_id():
        return self.email
   



