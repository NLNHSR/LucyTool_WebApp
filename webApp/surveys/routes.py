from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from webApp import db
from webApp.models import Survey, User
from webApp.surveys.forms import SurveyForm

surveys = Blueprint('surveys', __name__)
 
@surveys.route("/survey/new/<users>", methods=['GET', 'POST'])
@login_required 
def new_survey(users):
    form = SurveyForm()
    if form.validate_on_submit():
        survey = Survey(title=form.title.data, description=form.description.data, incentive=form.incentive.data, link=form.link.data, assigned_to=form.assigned_to.data, author=current_user)
        db.session.add(survey) 
        db.session.commit()
        flash('Your Survey has been created!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        ids = ""
        emails = None
        import re
        import numpy
        pattern = re.compile(r"\'([^)]*)\'")
        emails = numpy.array(pattern.findall(users))
        nEmails = []
        for email in emails:
            nEmails += email.split(',')
        sEmails = []
        for email in nEmails:
            email = email.strip()
            email = email[1:len(email)-1]
            if('@' in email):
                sEmails.append(email)                    

        search = User.query.all()
        for user in search:
            if user.email in sEmails:
                ids += str(user.user_id) + ","

        form.assigned_to.data = ids

    return render_template('create_survey.html', title='New Survey', form=form, legend='New Survey')

@surveys.route("/survey/<int:survey_id>")
def survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    return render_template('survey.html', title=survey.title, survey=survey)


@login_required
@surveys.route("/survey/<int:survey_id>/update", methods=['GET', 'POST'])
def update_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if survey.author != current_user:
        abort(403)
    form = SurveyForm()
    if form.validate_on_submit():
        survey.title = form.title.data
        survey.description=form.description.data
        survey.incentive=form.incentive.data
        survey.link=form.link.data
        survey.assigned_to=form.assigned_to.data
        db.session.commit()
        flash('Your survey has been updated', 'success')
        return redirect(url_for('surveys.survey', survey_id=survey.id))
    elif request.method == 'GET':
        form.title.data = survey.title
        form.description.data = survey.description
        form.incentive.data = survey.incentive
        form.link.data = survey.link
        form.assigned_to.data = survey.assigned_to

    return render_template('create_survey.html', title='Update Survey', form=form, legend='Update Survey')

@login_required
@surveys.route("/survey/<int:survey_id>/delete", methods=['POST'])
def delete_survey(survey_id):
    survey = Survey.query.get_or_404(survey_id)
    if survey.author != current_user:
        abort(403)
    db.session.delete(survey)
    db.session.commit()
    flash('Your survey has been deleted!', 'success')
    return redirect(url_for('main.home'))

