from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    name = StringField('Enter Search Terms', validators=[DataRequired()])
    submit = SubmitField()