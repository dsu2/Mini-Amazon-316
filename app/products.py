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
bp = Blueprint('products', __name__)

class ExpensiveForm(FlaskForm):
    k = IntegerField('Priciest number', validators=[DataRequired(), NumberRange(min=1, max =300)])
    submit = SubmitField('sort')

@bp.route('/shelf', methods=['GET', 'POST'])
def shelf():
    # get all available products for sale:
    form = ExpensiveForm()
    if form.validate_on_submit():
        products = Product.get_expensive_k(True,form.k.data)
    else:
        products = Product.get_all(True)    
    
    return render_template('products.html',
                           avail_products=products,
                           form=form)

@bp.route('/<int:productid>/')
def productDetails(productid=None):
    products = Product.get(id=productid)
    return render_template('product_detailed.html', avail_products = products)