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
from .models.cart import Cart
from .models.inventory import Inventory


from flask import Blueprint

bp = Blueprint('index', __name__)
class ExpensiveForm(FlaskForm):
    k = IntegerField('Priciest number', validators=[DataRequired(), NumberRange(min=1, max =300)])
    submit = SubmitField('sort')

class ReviewForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1, max =10000)])
    submit = SubmitField('sort')

class CartForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1, max =10000)])
    submit = SubmitField('sort')

class InvForm(FlaskForm):
    sid = IntegerField('User/Seller ID', validators=[DataRequired(), NumberRange(min=0, max =10000)])
    submit = SubmitField('sort')

class PurForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=0, max =10000)])
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

    cform = CartForm()
    if cform.validate_on_submit():
        cart = Cart.get_cart(cform.uid.data)
    else:
        cart = Cart.get_all()

    iform = InvForm()
    if iform.validate_on_submit():
        inv = Inventory.get_by_sid(iform.sid.data)
    else:
        inv = Inventory.get_all()
    '''
    pform = PurForm()
    if pform.validate_on_submit():
        purch = Purchase.get_by_uid(pform.uid.data)
    else:
        purch = Purchase.get_all()

    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None 
    '''
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           #purchase_history=purchases,
                           recent_reviews = reviews,
                           form=form, rform = rform, cform = cform, iform = iform, user_cart = cart, user_inventory = inv)



#reviews part now?

"""
@bp.route('/', methods=['GET', 'POST'])
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    
    # find user any user has bought:
    
    form = ReviewForm()
    if form.validate_on_submit():
        reviews = ProductReview.get_5_recent_uid(form.uid.data)
    else:
        reviews = ProductReview.get_all()
    # find the products current user has bought:
    # if current_user.is_authenticated and form.validate_on_submit():
    #     '''
    #     code that was here before:
    #     purchases = Purchase.get_all_by_uid_since(
    #         current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    #     '''
    #     all_purchases = Purchase.get_every_purchase_by_uid(current_user.id)
    # else:
    #     all_purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products)


class PurchaseHistoryForm(FlaskForm):
    k = IntegerField('User ID?', validators=[DataRequired()])
    submit = SubmitField('Get Purchase History')

@bp.route('/purchase-history', methods=['GET','POST'])
def purchaseHistory():
    form = PurchaseHistoryForm()
    # find the purchases:
    if current_user.is_authenticated and form.validate_on_submit():
        '''
        code that was here before:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        '''
        all_purchases = Purchase.get_every_purchase_by_uid(form.data.k)
    else:
        all_purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           form=form)
    """
