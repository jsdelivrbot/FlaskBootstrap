from flask import Blueprint, render_template, abort, session
from jinja2 import TemplateNotFound
from flask import request, abort
from sqlalchemy import exc
from common.db import db, User


users = Blueprint('users', __name__,
                        template_folder='templates')


def handle_register_post(postdata):
    required = ["email", "password", "confirm_password", "first", "last"]
    for value in required:
        if value not in postdata.keys() or postdata[value] == "":
            abort(400, "%s missing or empty" % value)
    if postdata["password"] != postdata["confirm_password"]:
        abort(400, "Passwords do not match")
    user = User(postdata["email"], postdata["password"],
                   postdata["first"], postdata["last"])
    db.session.add(user)
    try:
        db.session.commit()
    except exc.IntegrityError:
        abort(400, "Email already exists")

    return "User created", 201


def handle_login_post(postdata):
    required = ["email", "password"]
    for value in required:
        if value not in postdata.keys() or postdata[value] == "":
            abort(400, "%s missing or empty" % value)
    user = User.query.filter_by(email=postdata["email"]).one()
    if user.compare_pass(postdata["password"]):
        return "User Logged in", 201
    else:
        abort(403, "Username and password don't match")

@users.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return handle_login_post(request.form)
    else:
        try:
            return render_template('users/login.html')
        except TemplateNotFound:
            abort(404)

@users.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return handle_register_post(request.form)
    try:
        return render_template('users/register.html')
    except TemplateNotFound:
        abort(404)
