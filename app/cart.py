from flask import Flask
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_sqlalchemy import SQLAlchemy
from .models.product import Product
from .models.purchase import Purchase
from .models.reviews import ProductReview
from .models.cart import Cart
from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('cart', __name__)

class CartForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1, max =10000)])
    submit = SubmitField('sort')
class CartRemoveForm(FlaskForm):
    submit = SubmitField('Delete')


@bp.route('/items', methods=['GET', 'POST'])
def items():
    cform = CartForm()
    if cform.validate_on_submit():
        cart = Cart.get_cart(cform.uid.data)
    else:
        cart = Cart.get_all()

    return render_template('cart.html',user_cart = cart, cform = cform)
'''
@bp.route('pid/<int:productid>/edititem/',methods=['GET','POST'])
def edititem(productid = None):
    cart = Cart.get(id=productid)
    removeform = CartRemoveForm()
'''

