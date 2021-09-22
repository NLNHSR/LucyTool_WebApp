from wtforms.validators import NoneOf
from webApp.surveys.forms import SurveyForm
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from webApp import db, bcrypt
from webApp.models import Survey, User, Post
from webApp.users.forms import (RegistrationForm, CompanyRegistrationForm, LoginForm,
                                   RequestResetForm, ResetPasswordForm, FilterForm, SingleSearch, UpdateCompany, UpdateTeenager)
from webApp.users.utils import save_picture, send_reset_email
from datetime import datetime

users = Blueprint('users', __name__)
 
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm() 
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_type='teenager', username=form.username.data, email=form.email.data, 
        password=hashed_password, first_name=form.first_name.data, last_name=form.last_name.data,
        age=form.age.data, city=form.city.data, state=form.state.data, birthday=form.birthday.data, 
        gender=form.gender.data, race=form.race.data, ethnicity=form.ethnicity.data, 
        religious_affiliation=form.religious_affiliation.data, political_affiliation=form.political_affiliation.data,
        social_class=form.social_class.data, sexuality=form.sexuality.data, hobbies=form.hobbies.data, 
        college_major=form.college_major.data, career_field=form.career_field.data, phone_number=form.phone_number.data, user_id=generate_id())
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

 
@users.route("/register/company", methods=['GET', 'POST'])
def register_company():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = CompanyRegistrationForm() 
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_type='company', username=form.username.data, email=form.email.data, password=hashed_password, 
        company_name=form.company_name.data, city=form.city.data, state=form.state.data, birthday=datetime.now(), user_id=generate_id())
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register_company.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login(): 
    #db.session.query(Model).delete()
    #db.session.commit()
    #db.drop_all()
    #db.create_all() 
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = None
    if current_user.user_type == "teenager":
        form = UpdateTeenager()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            #db.session.commit()
            current_user.age = form.age.data
            current_user.city = form.city.data
            current_user.state = form.state.data
            current_user.gender = form.gender.data
            current_user.religious_affiliation = form.religious_affiliation.data
            current_user.political_affiliation = form.political_affiliation.data
            current_user.social_class = form.social_class.data
            current_user.sexuality = form.sexuality.data
            current_user.hobbies = form.hobbies.data
            current_user.college_major = form.college_major.data
            current_user.career_field = form.career_field.data
            current_user.phone_number = form.phone_number.data
            db.session.commit()
            flash('Your account has been updated', 'success')
            return redirect(url_for('users.account'))

    elif current_user.user_type == "company":
        form = UpdateCompany()
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.company_name = form.company_name.data
            current_user.city = form.city.data
            current_user.state = form.state.data
            db.session.commit()
            flash('Your account has been updated', 'success')
            return redirect(url_for('users.account'))

    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.city.data = current_user. city
        form.state.data = current_user.state
        if current_user.user_type == 'teenager':
            form.age.data = current_user.age
            form.gender.data = current_user.gender
            form.religious_affiliation.data = current_user.religious_affiliation
            form.political_affiliation.data = current_user.political_affiliation
            form.social_class.data = current_user.social_class
            form.sexuality.data = current_user.sexuality
            form.hobbies.data = current_user.hobbies
            form.college_major.data = current_user.college_major
            form.career_field.data = current_user.career_field
            form.phone_number.data = current_user.phone_number
        elif current_user.user_type == "company":
            form.company_name.data = current_user.company_name
    else:
        print (form.errors)      

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=posts, user=user)


@users.route("/company/surveys/<string:username>")
def user_surveys(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    surveys = Survey.query.filter_by(author=user)\
        .order_by(Survey.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('company_surveys.html', surveys=surveys, user=user)


@users.route("/teenager/surveys/<string:username>")
def assigned_surveys(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    surveys = Survey.query.filter(Survey.assigned_to.contains(str(user.user_id)))\
        .order_by(Survey.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('teenager_surveys.html', surveys=surveys, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been send with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@users.route("/filter", methods=['GET', 'POST'])
def filter():
    form = FilterForm() 
    if form.validate_on_submit():
        users = User.query.filter(User.user_type == 'teenager')
        #if form.first_name.data != None:
        #    users = User.query.filter(User.first_name.contains(str(form.first_name.data)))
        #if form.last_name.data != None:
        #    users = users.filter(User.last_name.contains(str(form.last_name.data)))
        
        if form.age1.data != None and form.age2.data != None:
            users = User.query.filter((User.age >= form.age1.data) & (User.age <= form.age2.data)).all()

        if form.city.data:
            #users = User.query.filter(str(User.city).strip().upper() == str(form.city.data).strip().upper()).all() 
            for user in users:
                if not user.city.strip().upper() == str(form.city.data.strip().upper()):
                    users.remove(user)
        
        if form.state.data:
            #users = User.query.filter(str(User.state).strip().upper() == str(form.state.data).strip().upper()).all() 
            for user in users:
                if not user.state.strip().upper() == str(form.state.data.strip().upper()):
                    users.remove(user)

        if form.gender.data:
            #users = User.query.filter(User.gender in form.gender.data).all() 
            for user in users:
                if not user.gender in form.gender.data:
                    users.remove(user)

        if form.race.data:
            #users = User.query.filter(User.race in form.race.data).all() 
            for user in users:
                if not user.race in form.race.data:
                    users.remove(user)

        if form.ethnicity.data:
            #users = User.query.filter(User.ethnicity in form.ethnicity.data).all() 
            for user in users:
                if not user.ethnicity in form.ethnicity.data:
                    users.remove(user)

        if form.religious_affiliation.data:
            #users = User.query.filter(User.religious_affiliation in form.religious_affiliation.data).all() 
            for user in users:
                if not user.religious_affiliation in form.religious_affiliation.data:
                    users.remove(user)

        if form.political_affiliation.data:
            #users = User.query.filter(User.political_affiliation in form.political_affiliation.data).all() 
            for user in users:
                if not user.political_affiliation in form.political_affiliation.data:
                    users.remove(user)

        if form.social_class.data:
            #users = User.query.filter(User.social_class in form.social_class.data).all() 
            for user in users:
                if not user.social_class in form.social_class.data:
                    users.remove(user)

        if form.sexuality.data:
            #users = User.query.filter(User.sexuality in form.sexuality.data).all() 
            for user in users:
                if not user.sexuality in form.sexuality.data:
                    users.remove(user)

        #return redirect(url_for('users.filter_results'))
        return render_template('filter_results.html', users=users)
    return render_template('filter_search.html', title='Filter', form=form)

@users.route("/filter/results", methods=['GET', 'POST'])
def filter_results():
    users = User.query.all()
    print(users)
    return render_template('filter_results.html', users=users)

@users.route("/search", methods=['GET', 'POST'])
def single_search():
    form = SingleSearch() 
    if form.validate_on_submit():
        #users = User.query.filter(str(User.user_id).strip == str(form.id.data).strip)
        users = User.query.all()
        user_found = None
        for user in users:
            if user.user_id == form.id.data:
                user_found = user
        #return redirect(url_for('users.filter_results'))
        return render_template('single_results.html', user=user_found)
    return render_template('single_search.html', title='Search Users', form=form)


def generate_id():
    import random

    id = (''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8)))
    user = User.query.filter(Survey.user_id == id).first()
    while(user):
        id = (''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8)))
        user = User.query.filter(Survey.user_id == id).first()

    return id
