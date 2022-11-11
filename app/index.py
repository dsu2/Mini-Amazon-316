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
                           cform = cform, iform = iform, user_cart = cart, user_inventory = inv, pform = pform, user_purchases = purch)
