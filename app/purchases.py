from flask import render_template, redirect, url_for, flash, request
from sqlalchemy import false
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

bp = Blueprint('purchases', __name__)

'''
class PurForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=0, max =10000)])
    submit = SubmitField('Show Purchase History')
'''

@bp.route('/your-purchases', methods=['GET', 'POST'])
def yourPurchases():
    # pform = PurForm()
    # access purchases via inputting user id
    if current_user.is_authenticated:
        all_user_purchases = Purchase.get_by_uid(current_user.id)
    
    else:
        all_user_purchases = None 
    
    return render_template('purchases.html',
                           purchase_history=all_user_purchases)

@bp.route('/<int:purchaseid>/')
def purchaseDetails(purchaseid=None):
    purchase_specifics = Purchase.get(id=purchaseid)
    return render_template('purchase_detailed.html', purchase_specifics = purchase_specifics)

