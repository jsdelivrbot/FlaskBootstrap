from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea
from flask_wtf.file import FileField


class ProjectForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    excerpt = StringField(
        'excerpt',
        validators=[DataRequired(), Length(0, 500)],
        widget=TextArea())
    description = StringField(
        'body', validators=[DataRequired()], widget=TextArea())
    publish_date = DateField('Publish Date', format='%m/%d/%Y')
    thumbnail = FileField()


class ProjectImageForm(FlaskForm):
    caption = StringField('title', validators=[DataRequired()])
    image = FileField(validators=[DataRequired()])
