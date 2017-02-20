from flask_wtf import FlaskForm
from wtforms import StringField, TextField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('email', validators=[DataRequired()])
    body = TextField('password', validators=[DataRequired()])
