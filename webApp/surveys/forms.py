from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class SurveyForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    incentive = StringField('Incentive', validators=[DataRequired()])
    link =  StringField('Link', validators=[DataRequired()])
    assigned_to = TextAreaField('Assigned To', validators=[DataRequired()])
    submit = SubmitField('Create')

