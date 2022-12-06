from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from flask_paginate import Pagination, get_page_parameter, get_page_args
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

import sys

from .models.user import User
from .models.purchase import Purchase
from .models.reviews import ProductReview
from .models.reviews import SellerReview
from .models.seller import Seller


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
    address = StringField('Street Address', validators = [DataRequired()])
    city = StringField('City', validators = [DataRequired()])
    state = StringField('State/Province', validators = [DataRequired()])
    image = StringField('Link to image, .jpg, .png, and .gif only. Can leave empty if you want', validators = [])
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

class addMoneyForm(FlaskForm):
    new_value = DecimalField('', places =2, validators=[DataRequired(), NumberRange(min = 0)])
    submit = SubmitField('Add Amount')

class withdrawMoneyForm(FlaskForm):
    new_value = DecimalField('', places =2, validators=[DataRequired(), NumberRange(min = 0)])
    submit = SubmitField('Remove Amount')

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

class AddressEditForm(FlaskForm):
    new_address = StringField('Street Address', validators = [DataRequired()])
    new_city = StringField('City', validators = [DataRequired()])
    new_state = StringField('State/Province', validators = [DataRequired()])
    submit = SubmitField('Submit Changes')

class imageEditForm(FlaskForm):
    image = StringField('Link to new profile image. .jpg, .png, and .gif only', validators=[DataRequired()])
    submit = SubmitField('Submit Changes')

class addReviewForm(FlaskForm):
    text = StringField('Text for review', validators = [DataRequired()])
    val = IntegerField('Rating from 1-10', validators=[DataRequired(), NumberRange(min=1, max =10)])
    submit = SubmitField('Add Review')

class EditReviewForm(FlaskForm):
    text = StringField('New text for updated review', validators = [DataRequired()])
    val = IntegerField('New rating from 1-10', validators=[DataRequired(), NumberRange(min=1, max =10)])
    submit = SubmitField('Edit Review')

class RemoveReviewForm(FlaskForm):
    submit = SubmitField('Remove Review')

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
    user_info = None
    if current_user.is_authenticated:
        user_info = User.get(current_user.id)
    return render_template('profile.html', user_info=user_info)

#editing user info
@bp.route('/edit-name', methods=['GET', 'POST'])
def editName(userid = None):
    nameForm = nameEditForm()
    userid = current_user.get_id()
    if nameForm.validate_on_submit():
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
    if eForm.validate_on_submit():
        print('email Form is Valid', file=sys.stdout)
        print(eForm.new_email.data)
        User.editUserEmail(id=userid, email=eForm.new_email.data)
        if eForm.new_email.data:
            return redirect(url_for('users.profile'))
    return render_template('change_email.html', eForm = eForm)

@bp.route('/edit-pfp', methods=['GET', 'POST'])
def editImage(userid = None):
    error = None
    eForm = imageEditForm()
    userid = current_user.get_id()
    if eForm.validate_on_submit():
        print('edit image Form is Valid', file=sys.stdout)
        ending = eForm.image.data[-4:]
        if ending == ".jpg" or ending == ".gif" or ending == ".png":
            User.editUserImage(id=userid, image=eForm.image.data)
            if eForm.image.data:
                return redirect(url_for('users.profile'))
        else:
            error = "You did not submit a link to a valid image type"
    return render_template('change_image.html', eForm = eForm, error=error)

@bp.route('/addMoney', methods=['GET', 'POST'])
def addMoney(userid = None):
    error = None
    eForm = addMoneyForm()
    userid = current_user.get_id()
    currentbal = User.getvalue(userid)
    if eForm.validate_on_submit():
        print('Money Form is valid', file=sys.stdout)
        print(eForm.new_value.data)
        if eForm.new_value.data >= 0:
            User.editAddBalance(id=userid, amount=eForm.new_value.data)
            if eForm.new_value.data:
                return redirect(url_for('users.profile'))
        else:
            error = "Cannot add a negative amount! Try to withdraw instead"
    return render_template('addMoney.html', eForm = eForm, currentbal=currentbal, error=error)

@bp.route('/withdrawMoney', methods=['GET', 'POST'])
def withdrawMoney(userid = None):
    error = ''
    eForm = withdrawMoneyForm()
    userid = current_user.get_id()
    currentbal = User.getvalue(userid)
    if eForm.validate_on_submit():
        print('Money Form is valid', file=sys.stdout)
        print(eForm.new_value.data)
        if eForm.new_value.data != None:
            if eForm.new_value.data >= 0:
                if User.getvalue(userid) >= eForm.new_value.data:
                    User.editAddBalance(id=userid, amount= -1*eForm.new_value.data)
                    return redirect(url_for('users.profile'))
                else:
                    error = "You can't withdraw more money than what is in your account!"
            else:
                error = "You can't withdraw a negative amount! Try to deposit instead."
                print("SQUIDWARD GAMING", file = sys.stdout)
    else:
        error = "You have entered an invalid amount."
    return render_template('withdrawMoney.html', eForm = eForm, error = error, currentbal=currentbal)


@bp.route('/edit-address', methods=['GET', 'POST'])
def editAddress(userid = None):
    aForm = AddressEditForm()
    userid = current_user.get_id()
    if aForm.validate_on_submit():
        print('Address Form is Valid', file=sys.stdout)
        print(aForm.new_address.data)
        print(aForm.new_city.data)
        print(aForm.new_state.data)
        User.editUserAddress(id=userid, address= aForm.new_address.data, city = aForm.new_city.data, state = aForm.new_state.data)
        if aForm.new_address.data:
            return redirect(url_for('users.profile'))
    return render_template('change_address.html', aForm = aForm)

@bp.route('/edit-password', methods=['GET', 'POST'])
def editPassword(userid = None):
    pwForm = passwordEditForm()
    userid = current_user.get_id()

    if pwForm.validate_on_submit():
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
        if form.image.data == '':
            print("yeah it empty", file = sys.stdout)
            form.image.data = "https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"
        ending = form.image.data[-4:]
        if ending == ".jpg" or ending == ".gif" or ending == ".png":
            print("Hooray", file = sys.stdout)
            print(form.image.data, file = sys.stdout)
            if User.register(form.email.data,
                            form.password.data,
                            form.firstname.data,
                            form.lastname.data,
                            form.address.data,
                            form.city.data,
                            form.state.data,
                            form.image.data):
                flash('Congratulations, you are now a registered user!')
                return redirect(url_for('users.login'))
            else:
                flash('There was an error...')
    return render_template('register.html', title='Register', form=form)

@bp.route('/profile/<int:userid>', methods=['GET', 'POST'])
def publicprofile(userid = None):
    errorReview = ''
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page=10

    avgreview = None
    numreview = None

    form = None

    user_info = User.get(userid)
    userreviews = ProductReview.get_all_by_uid(userid)
    pagination_userreviews = None
    userpagination = None
    if userreviews != None:
        pagination_userreviews=userreviews[offset:offset+per_page]
        userpagination = Pagination(page=page, total=len(userreviews), record_name='product reviews', per_page=per_page)

    sellerid = Seller.get_sid(userid)
    if sellerid != None:
        form = addReviewForm()
        if form.validate_on_submit():
            if current_user.get_id() != None and len(Purchase.get_by_uid_sid(uid=current_user.get_id(), sid = sellerid) )!= 0:
                result = SellerReview.addSellerReview(sid = sellerid, uid = current_user.get_id(), text = form.text.data, rating = form.val.data)  
                if result == None:
                    errorReview = "You have reviewed this seller."
            else:
                errorReview = "You cannot review this seller because you did not purchase an item from them!"
    print(errorReview, file = sys.stdout)
    sellerreviews = None
    pagination_sellerreviews= None
    sellerpagination = None
    sellerid = Seller.get_sid(userid)
    if sellerid != None:
        sellerreviews = SellerReview.get_all_by_sid(sellerid)
        pagination_sellerreviews = sellerreviews[offset:offset+per_page]
        print(pagination_sellerreviews, file = sys.stdout)
        sellerpagination = Pagination(page=page, total=len(sellerreviews), record_name='seller reviews', per_page=per_page)
        if avgreview!= None:
            avgreview = round(SellerReview.findAvgRating(sid=sellerid), 2)
        numreview = SellerReview.findNumReview(sid=sellerid)
   
    return render_template('publicprofile.html', user_info=user_info, userpagination = userpagination, \
        sellerpagination = sellerpagination, userreviews = pagination_userreviews, sellerid = sellerid, \
        avgreview = avgreview, numreview = numreview, sellerreviews=pagination_sellerreviews, form = form, \
        errorReview = errorReview)

@bp.route('/profile/<int:sellersuserid>/editreview/', methods=['GET', 'POST'])
def editReview(sellersuserid = None):
    userid = current_user.get_id()
    editform = EditReviewForm()
    removeform = RemoveReviewForm()
    if editform.validate_on_submit():
        SellerReview.editSellerReview(sid = Seller.get_sid(sellersuserid), uid = userid, text = editform.text.data, rating = editform.val.data)
        return redirect(url_for('users.publicprofile', userid = sellersuserid))
   
    if removeform.validate_on_submit():
        print('Remove form is Valid', file=sys.stdout)
        SellerReview.removeSellerReview(sid = Seller.get_sid(sellersuserid), uid = userid)
        return redirect(url_for('users.publicprofile', userid = sellersuserid))

    return render_template('edit_seller_review.html', editform = editform, removeform = removeform, sellersuserid = sellersuserid)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/register-seller')
def registerSeller():
    if current_user.is_authenticated:
        user_info = User.get(current_user.id)
    Seller.registerSeller(current_user.id)
    return render_template('profile.html', user_info=user_info)

