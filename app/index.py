from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange

from .models.product import Product
from .models.purchase import Purchase
from .models.reviews import ProductReview

from flask import Blueprint
bp = Blueprint('index', __name__)

class ExpensiveForm(FlaskForm):
    k = IntegerField('priciest', validators=[DataRequired(), NumberRange(min=1, max =300)])
    submit = SubmitField('sort')

class ReviewForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1, max =10000)])
    submit = SubmitField('sort')

@bp.route('/', methods=['GET', 'POST'])
def index():
    # get all available products for sale:
    form = ExpensiveForm()
    if form.validate_on_submit():
        products = Product.get_expensive_k(True,form.k.data)
    else:
        products = Product.get_all(True)
    rform = ReviewForm()
    if rform.validate_on_submit():
        reviews = ProductReview.get_5_recent_uid(rform.uid.data)
    else:
        reviews = ProductReview.get_all()
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           recent_reviews = reviews,
                           form=form, rform = rform)


#reviews part now?

"""
@bp.route('/', methods=['GET', 'POST'])
def index():
    # get all available products for sale:
    form = ReviewForm()
    if form.validate_on_submit():
        reviews = ProductReview.get_5_recent_uid(form.uid.data)
    else:
        reviews = ProductReview.get_all()
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           form=form)
    """