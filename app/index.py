from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.product import Product
from .models.purchase import Purchase



from flask import Blueprint

bp = Blueprint('index', __name__)

@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(True)
    
    # find user any user has bought:
    
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
    return render_template('purchases.html',
                        purchase_history=all_purchases,
                        form = form)                       
