from flask import Blueprint, render_template, abort
from flask import redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from sqlalchemy import exc
from common.db import db, User
from common.login import UserLogin, AuthException
from common.login import login_user, logout_user, login_required


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField(
        'password',
        validators=[
            DataRequired(),
            EqualTo('confirm_password', message='Passwords must match')
        ]
    )
    confirm_password = PasswordField('confirm password',
                                     validators=[DataRequired()])
    first = StringField('first', validators=[DataRequired()])
    last = StringField('last', validators=[DataRequired()])


users = Blueprint('users', __name__,
                  template_folder='templates')


def handle_register_post(postdata):
    required = ["email", "password", "confirm_password", "first", "last"]
    for value in required:
        if value not in postdata.keys() or postdata[value] == "":
            abort(400, "%s missing or empty" % value)
    if postdata["password"] != postdata["confirm_password"]:
        abort(400, "Passwords do not match")


@users.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserLogin()
        try:
            user.login(form.email.data, form.password.data)
            login_user(user)
            return redirect("/")
        except AuthException:
            form.password.errors.append("invalid email or password")
    return render_template(
        'form.html',
        form=form,
        btn_label="Login",
        path=request.url_rule,
        method="post")


@users.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/")


@users.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.email.data,
                    form.password.data,
                    form.first.data,
                    form.last.data)
        db.session.add(user)
        try:
            db.session.commit()
            return redirect("/")
        except exc.IntegrityError:
            form.email.errors.append("Email already exists")
    return render_template(
        'form.html',
        form=form,
        btn_label="Register",
        path=request.url_rule,
        method="post")
