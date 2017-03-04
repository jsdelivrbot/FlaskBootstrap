from flask_login import LoginManager
# expose these for import(allows us to make our own if we change login methods)
from flask_login import login_user, logout_user, login_required, current_user # NOQA
import sqlalchemy
from common.db import User

login_manager = LoginManager()


class AuthException(Exception):
    pass


@login_manager.user_loader
def load_user(email):
    return UserLogin.load(email)


class UserLogin(object):
    def __init__(self):
        self.uid = None

    def login(self, email, password):
        try:
            user = User.query.filter_by(email=email).one()
        except sqlalchemy.orm.exc.NoResultFound:
            raise AuthException("Email not found")

        if not user.compare_pass(password):
            raise AuthException("Invalid username or password")
        self.uid = user.id
        self.email = user.email
        self.first = user.first
        self.last = user.last

    @staticmethod
    def load(email):
        try:
            user = User.query.filter_by(email=email).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None
        user = User.query.filter_by(email=email).one()
        ul = UserLogin()
        ul.uid = user.id
        ul.email = user.email
        ul.first = user.first
        ul.last = user.last
        return ul

    def get_db(self):
        try:
            user = User.query.filter_by(id=self.uid).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None
        return user

    def is_authenticated(self):
        return self.uid is not None

    def is_active(self):
        return True

    def is_anonymous(self):
        return self.uid is None

    def get_id(self):
        return self.email
