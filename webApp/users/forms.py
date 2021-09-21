from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import IntegerField, SelectField, SelectMultipleField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from webApp.models import User
import geonamescache


class RegistrationForm(FlaskForm):
    user_id = StringField('User Id')
    username = StringField('Username',  
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name',  
                            validators=[DataRequired(), Length(min=1, max=50)])    
    age = IntegerField('Age', 
                        validators=[DataRequired()])
    city = StringField('City',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    #gc = geonamescache.GeonamesCache()
    #city = SelectField(
    #    'City',
    #    choices=gc.get_cities()
    #)                        
    state = StringField('State',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    birthday = DateField('Birthday', 
                            validators=[DataRequired()])
    gender = SelectField(
        'Gender',
        choices=[('f', 'Female'), ('m', 'Male'), ('gf', 'Genderfluid'), ('a', 'Agender'), 
        ('tf', 'Transgender Female'), ('tm', 'Transgender Male'), ('i', 'Intersex'), 
        ('nb', 'Nonbinary'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    race = SelectField(
        'Race',
        choices=[('aian', 'American Indian or Alaska Native'), ('a', 'Asian'), ('baa', 'Black or African American'), ('hl', 'Hispanic or Latino'), 
        ('nhpi', 'Native Hawaiian or Other Pacific Islander'), ('w', 'White'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    ethnicity = SelectField(
        'Ethnicity',
        choices=[('hl', 'Hispanic or Latino'), ('nhl', 'Not Hispanic or Latino'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    religious_affiliation = SelectField(
        'Religious Affiliation',
        choices=[('c', 'Christian'), ('m', 'Muslim'), ('j', 'Jewish'), ('h', 'Hindu'), ('b', 'Buddhist'), 
        ('ar', 'Ancient Religion'), ('at', 'Athiest'), ('ag', 'Agnostic'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    political_affiliation = SelectField(
        'Political Affiliation',
        choices=[('d', 'Democratic'), ('r', 'Republican'), ('i', 'Independent'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    social_class = SelectField(
        'Social Class',
        choices=[('u', 'Upper'), ('um', 'Upper-Middle'), ('m', 'Middle'), ('w', 'Working'), ('l', 'Lower'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    sexuality = SelectField(
        'Sexuality',
        choices=[('h', 'Heterosexual'), ('g', 'Gay/Lesbian'), ('b', 'Bisexual'), ('p', 'Pansexual'), ('a', 'Asexual'), ('q', 'Queer'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    hobbies = StringField('Hobby(ies) (Comma Seperated)',  
                            validators=[])
    college_major = StringField('Prospective College Major(s) (Comma Seperated)',  
                            validators=[])
    career_field = StringField('Prospective Career Field(s) (Comma Seperated)',  
                            validators=[])
    phone_number = StringField('Phone Number', 
                        validators=[DataRequired()])    
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user: 
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

class UpdateTeenager(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    age = IntegerField('Age', 
                        validators=[DataRequired()])
    city = StringField('City',  
                            validators=[DataRequired(), Length(min=1, max=50)])                     
    state = StringField('State',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    gender = SelectField(
        'Gender',
        choices=[('f', 'Female'), ('m', 'Male'), ('gf', 'Genderfluid'), ('a', 'Agender'), 
        ('tf', 'Transgender Female'), ('tm', 'Transgender Male'), ('i', 'Intersex'), 
        ('nb', 'Nonbinary'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    religious_affiliation = SelectField(
        'Religious Affiliation',
        choices=[('c', 'Christian'), ('m', 'Muslim'), ('j', 'Jewish'), ('h', 'Hindu'), ('b', 'Buddhist'), 
        ('ar', 'Ancient Religion'), ('at', 'Athiest'), ('ag', 'Agnostic'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    political_affiliation = SelectField(
        'Political Affiliation',
        choices=[('d', 'Democratic'), ('r', 'Republican'), ('i', 'Independent'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    social_class = SelectField(
        'Social Class',
        choices=[('u', 'Upper'), ('um', 'Upper-Middle'), ('m', 'Middle'), ('w', 'Working'), ('l', 'Lower'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    sexuality = SelectField(
        'Sexuality',
        choices=[('h', 'Heterosexual'), ('g', 'Gay/Lesbian'), ('b', 'Bisexual'), ('p', 'Pansexual'), ('a', 'Asexual'), ('q', 'Queer'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    hobbies = StringField('Hobby(ies) (Comma Seperated)',  
                            validators=[])
    college_major = StringField('Prospective College Major(s) (Comma Seperated)',  
                            validators=[])
    career_field = StringField('Prospective Career Field(s) (Comma Seperated)',  
                            validators=[])
    phone_number = StringField('Phone Number', 
                        validators=[DataRequired()])    
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user == current_user:
            return
        if user: 
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user == current_user:
            return 
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

class UpdateCompany(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    city = StringField('City',  
                            validators=[DataRequired(), Length(min=1, max=50)])                     
    state = StringField('State',  
                            validators=[DataRequired(), Length(min=1, max=50)])  
    company_name = StringField('Company Name',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user == current_user:
            return 
        if user: 
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user == current_user:
            return 
        if user:
            raise ValidationError('That email is taken. Please choose a different one')



class CompanyRegistrationForm(FlaskForm):
    username = StringField('Username',  
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    company_name = StringField('Company Name',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    city = StringField('City',  
                            validators=[DataRequired(), Length(min=1, max=50)])                    
    state = StringField('State',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user: 
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class FilterForm(FlaskForm):
    id = IntegerField('ID', default=-1)
    age1 = IntegerField('A1', default=13)
    age2 = IntegerField('A2', default=19)
    city = StringField('City')                    
    state = StringField('State')
    birthday = DateField('Birthday')
    gender = SelectMultipleField( 
        'Gender',
        choices=[('f', 'Female'), ('m', 'Male'), ('gf', 'Genderfluid'), ('a', 'Agender'), 
        ('tf', 'Transgender Female'), ('tm', 'Transgender Male'), ('i', 'Intersex'), 
        ('nb', 'Nonbinary'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')])
    race = SelectMultipleField(
        'Race',
        choices=[('aian', 'American Indian or Alaska Native'), ('a', 'Asian'), ('baa', 'Black or African American'), ('hl', 'Hispanic or Latino'), 
        ('nhpi', 'Native Hawaiian or Other Pacific Islander'), ('w', 'White'), ('pnts', 'Prefer Not To Say')])
    ethnicity = SelectMultipleField(
        'Ethnicity',
        choices=[('hl', 'Hispanic or Latino'), ('nhl', 'Not Hispanic or Latino'), ('pnts', 'Prefer Not To Say')])
    religious_affiliation = SelectMultipleField(
        'Religious Affiliation',
        choices=[('c', 'Christian'), ('m', 'Muslim'), ('j', 'Jewish'), ('h', 'Hindu'), ('b', 'Buddhist'), 
        ('ar', 'Ancient Religion'), ('at', 'Athiest'), ('ag', 'Agnostic'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')])
    political_affiliation = SelectMultipleField(
        'Political Affiliation',
        choices=[('d', 'Democratic'), ('r', 'Republican'), ('i', 'Independent'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')])
    social_class = SelectMultipleField(
        'Social Class',
        choices=[('u', 'Upper'), ('um', 'Upper-Middle'), ('m', 'Middle'), ('w', 'Working'), ('l', 'Lower'), ('pnts', 'Prefer Not To Say')])
    sexuality = SelectMultipleField(
        'Sexuality',
        choices=[('h', 'Heterosexual'), ('g', 'Gay/Lesbian'), ('b', 'Bisexual'), ('p', 'Pansexual'), ('a', 'Asexual'), ('q', 'Queer'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')])
    hobbies = StringField('Hobby(ies) (Comma Seperated)')
    college_major = StringField('Prospective College Major(s) (Comma Seperated)')
    career_field = StringField('Prospective Career Field(s) (Comma Seperated)')

    submit = SubmitField('Filter')

'''
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    first_name = StringField('First Name',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name',  
                            validators=[DataRequired(), Length(min=1, max=50)])    
    age = IntegerField('Age', 
                        validators=[DataRequired()])
    city = StringField('City',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    #gc = geonamescache.GeonamesCache()
    #city = SelectField(
    #    'City',
    #    choices=gc.get_cities()
    #)                        
    state = StringField('State',  
                            validators=[DataRequired(), Length(min=1, max=50)])
    birthday = DateField('Birthday', 
                            validators=[DataRequired()])
    gender = SelectField(
        'Gender',
        choices=[('f', 'Female'), ('m', 'Male'), ('gf', 'Genderfluid'), ('a', 'Agender'), 
        ('tf', 'Transgender Female'), ('tm', 'Transgender Male'), ('i', 'Intersex'), 
        ('nb', 'Nonbinary'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    race = SelectField(
        'Race',
        choices=[('aian', 'American Indian or Alaska Native'), ('a', 'Asian'), ('baa', 'Black or African American'), ('hl', 'Hispanic or Latino'), 
        ('nhpi', 'Native Hawaiian or Other Pacific Islander'), ('w', 'White'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    ethnicity = SelectField(
        'Ethnicity',
        choices=[('hl', 'Hispanic or Latino'), ('nhl', 'Not Hispanic or Latino'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    religious_affiliation = SelectField(
        'Religious Affiliation',
        choices=[('c', 'Christian'), ('m', 'Muslim'), ('j', 'Jewish'), ('h', 'Hindu'), ('b', 'Buddhist'), 
        ('ar', 'Ancient Religion'), ('at', 'Athiest'), ('ag', 'Agnostic'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    political_affiliation = SelectField(
        'Political Affiliation',
        choices=[('d', 'Democratic'), ('r', 'Republican'), ('i', 'Independent'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    social_class = SelectField(
        'Social Class',
        choices=[('u', 'Upper'), ('um', 'Upper-Middle'), ('m', 'Middle'), ('w', 'Working'), ('l', 'Lower'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    sexuality = SelectField(
        'Sexuality',
        choices=[('h', 'Heterosexual'), ('g', 'Gay/Lesbian'), ('b', 'Bisexual'), ('p', 'Pansexual'), ('a', 'Asexual'), ('q', 'Queer'), ('o', 'Other'), ('pnts', 'Prefer Not To Say')],
        validators=[DataRequired()])
    hobbies = StringField('Hobby(ies) (Comma Seperated)',  
                            validators=[])
    college_major = StringField('Prospective College Major(s) (Comma Seperated)',  
                            validators=[])
    career_field = StringField('Prospective Career Field(s) (Comma Seperated)',  
                            validators=[])
    phone_number = StringField('Phone Number', 
                        validators=[DataRequired()])   
    company_name = StringField('Company Name',  
                            validators=[DataRequired(), Length(min=1, max=50)])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one')
'''

class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
