from datetime import datetime
from enum import unique
from itertools import filterfalse
from os import name, replace, stat_result
from typing import AsyncGenerator
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from webApp import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))
 
class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10), unique=True, nullable=False, default='User ID')
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    # make sure to db.drop_all and db.create_all when you add/delete/edit fields 
    user_type = db.Column(db.String(20), nullable=False, default='') 
    
    age = db.Column(db.Integer, default=float("nan"))

    city = db.Column(db.String(100), nullable=False, default='')
    state = db.Column(db.String(50), nullable=False, default='')

    # For teens
    first_name = db.Column(db.String(50), nullable=False, default='')
    last_name = db.Column(db.String(50), nullable=False, default='')

    birthday = db.Column(db.DateTime, nullable=False, default=0)
    gender = db.Column(db.String(20), nullable=False, default='')
    race = db.Column(db.String(50), nullable=False, default='')
    ethnicity = db.Column(db.String(50), nullable=False, default='')
    religious_affiliation = db.Column(db.String(50), nullable=False, default='')
    political_affiliation = db.Column(db.String(50), nullable=False, default='')
    social_class = db.Column(db.String(20), nullable=False, default='')
    sexuality = db.Column(db.String(20), nullable=False, default='')
    hobbies = db.Column(db.Text, nullable=False, default='')
    college_major = db.Column(db.Text, nullable=False, default='')
    career_field = db.Column(db.Text, nullable=False, default='')
    phone_number = db.Column(db.String(20), unique=True, nullable=False, default='')
    surveys = db.Column(db.Text, nullable=True)

    # For companies
    company_name = db.Column(db.String(50), nullable=False, default='')
    surveys = db.relationship('Survey', backref='author', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post ('{self.title}', '{self.date_posted}')"

class Survey(db.Model):        
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    incentive = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    assigned_to = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Survey ('{self.title}', '{self.date_posted}')"
