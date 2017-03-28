from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from users import users
from blog import blog
from images import images
from portfolio import portfolio
from admin import admin
from common.db import db
from common.login import login_manager
import os


DB_USER = "docker"
DB_PASS = "docker"
DB_HOST = "mysql"
DB_PORT = "3306"
DATABASE = "blog"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'\
    .format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)

db.init_app(app)
migrate = Migrate(app, db)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

login_manager.init_app(app)
app.register_blueprint(users)
app.register_blueprint(images, url_prefix="/images")
app.register_blueprint(blog, url_prefix="/blog")
app.register_blueprint(portfolio, url_prefix="/portfolio")
app.register_blueprint(admin, url_prefix="/admin")


@app.errorhandler(403)
@app.errorhandler(401)
def error403_login(e):
    return redirect(url_for("users.login"))


if os.path.exists(".session_key"):
    with open(".session_key", "rb") as f:
        app.secret_key = f.read()
else:
    key = os.urandom(24)
    try:
        with open(".session_key", "wb+") as f:
            f.write(key)
        print("New session key generated")
        app.secret_key = key
    except IOError:
        print("Could not open session key file for writing")
        print("Generate your own with os.urandom(24) and",)
        print("write it to .session_key")
