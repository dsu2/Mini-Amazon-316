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
from .models.user import User
from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('cart', __name__)
'''
class CartForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1, max =10000)])
    submit = SubmitField('sort')
'''

@bp.route('/items', methods=['GET', 'POST'])
def items():
    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
        total = 0
        for item in cart:
            total += item.subtotal
    else:
        cart = Cart.get_all()

    return render_template('cart.html',user_cart = cart, total=total)

@bp.route('/delete/<int:pid>' ,methods=['GET','POST'])
def remove(pid):
    cart = Cart.delete_item(pid)
    'cform = CartForm()'
    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
        total = 0
        for item in cart:
            total += item.subtotal
    else:
        cart = Cart.get_all()

    return render_template('cart.html', user_cart=cart, total=total)

@bp.route('/edit_num/<int:pid>' ,methods=['GET','POST'])
def edit_num(pid):
    'cform = CartForm()'
    if 'quantity' in request.form:
        quantity = request.form['quantity']
        Cart.edit_num_item(pid, quantity)
    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
        total = 0
        for item in cart:
            total += item.subtotal
    else:
        cart = Cart.get_all()

    return render_template('cart.html', user_cart=cart, total=total)

@bp.route('/submit_cart/<int:pid>' ,methods=['GET','POST'])
def submit_cart(pid):
    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
        total = 0
        for item in cart:
            item.delete_item(pid)

    return render_template('cart.html', cart=cart, total=total)
