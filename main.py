from flask import Flask
from flask_migrate import Migrate
from users import users
from common.db import db
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

app.register_blueprint(users)

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
