from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    body = StringField('body', validators=[DataRequired()], widget=TextArea())
    publish_date = DateField('Publish Date', format='%m/%d/%Y')
