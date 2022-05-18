from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    body = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')