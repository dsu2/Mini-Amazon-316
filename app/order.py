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
from .models.order import Order
from .models.user import User
from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('order', __name__)
'''
class CartForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1, max =10000)])
    submit = SubmitField('sort')
'''
global total
@bp.route('/item', methods=['GET', 'POST'])
def item():
    if current_user.is_authenticated:
        order = Order.get_order(current_user.id)
        total = 0
        for item in order:
            total += item.subtotal
    return render_template('order.html', order = order, total=total)