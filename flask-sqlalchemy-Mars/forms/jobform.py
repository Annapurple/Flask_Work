from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    title = StringField('Job title', validators=[DataRequired()])
    team_leader_id = IntegerField('Team leader', validators=[DataRequired()])
    work = IntegerField('Work size', validators=[DataRequired()])
    collaborator = StringField('Collaborators', validators=[DataRequired()])
    is_job = BooleanField("Is job finished?")
    submit = SubmitField('Submit')