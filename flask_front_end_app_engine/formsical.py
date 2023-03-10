from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class PodcastSearchForm(FlaskForm):
    name = StringField('Enter Search Terms', validators=[DataRequired()])
    submit = SubmitField()

class RSSDownloadForm(FlaskForm):
    name = StringField('Enter RSS Feed', validators=[DataRequired()])
    submit = SubmitField()