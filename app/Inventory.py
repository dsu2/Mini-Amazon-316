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
bp = Blueprint('inventory', __name__)

class InvForm(FlaskForm):
    sid = IntegerField('User/Seller ID', validators=[DataRequired(), NumberRange(min=0, max =10000)])
    submit = SubmitField('sort')

@bp.route('/prod', methods=['GET', 'POST'])
def prod():
    iform = InvForm()
    if iform.validate_on_submit():
        inv = Inventory.get_by_sid(iform.sid.data)
    else:
        inv = Inventory.get_all()

    return render_template('inventory.html',user_inventory = inv, iform = iform)

@bp.route('/delete/<int:pid>' ,methods=['GET','POST'])
def remove(pid):
    inv = Inventory.delete(pid)
    iform = InvForm()
    if iform.validate_on_submit():
        inv = Inventory.get_by_sid(iform.sid.data)
    else:
        inv = Inventory.get_all()

    return render_template('inventory.html',user_inventory = inv, iform = iform)