from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

import sys

from .models.user import User


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#registration form
class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

#email editing form
class emailEditForm(FlaskForm):
    new_email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit Changes')

#first name editing form
class nameEditForm(FlaskForm):
    new_firstname = StringField('First Name', validators=[DataRequired()])
    new_lastname = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Submit Changes')

#password editing form   
class passwordEditForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password2 = PasswordField(
        'Repeat New Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Submit Changes')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

#profile page
@bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        user_info = User.get(current_user.id)
    return render_template('profile.html', user_info=user_info)

#editing user info
@bp.route('/edit-name', methods=['GET', 'POST'])
def editName(userid = None):
    nameForm = nameEditForm()
    userid = current_user.get_id()
    if nameForm.validate_on_submit:
        print('name Form is Valid', file=sys.stdout)
        print(nameForm.new_firstname.data)
        User.editUserName(id=userid, firstname=nameForm.new_firstname.data, lastname=nameForm.new_lastname.data)
        if nameForm.new_firstname.data and nameForm.new_lastname.data:
            return redirect(url_for('users.profile'))
    return render_template('edit_name.html', nameForm=nameForm)

@bp.route('/edit-email', methods=['GET', 'POST'])
def editEmail(userid = None):
    eForm = emailEditForm()
    userid = current_user.get_id()
    if eForm.validate_on_submit:
        print('email Form is Valid', file=sys.stdout)
        print(eForm.new_email.data)
        User.editUserEmail(id=userid, email=eForm.new_email.data)
        if eForm.new_email.data:
            return redirect(url_for('users.profile'))
    return render_template('change_email.html', eForm = eForm)

@bp.route('/edit-password', methods=['GET', 'POST'])
def editPassword(userid = None):
    pwForm = passwordEditForm()
    userid = current_user.get_id()

    if pwForm.validate_on_submit:
        print('password Form is Valid', file=sys.stdout)
        print(pwForm.new_password.data)
        if pwForm.new_password.data != pwForm.new_password2.data:
            flash('Passwords do not match!')
            return redirect(url_for('users.editPassword'))
        else:
            User.editUserPassword(id=userid, password=pwForm.new_password.data)
            if pwForm.new_password.data and pwForm.new_password2.data:
                return redirect(url_for('users.profile'))
    return render_template('change_password.html', pwForm = pwForm)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
