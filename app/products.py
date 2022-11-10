from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, AnyOf

from .models.product import Product
from .models.purchase import Purchase
from .models.reviews import ProductReview
from .models.cart import Cart
from .models.inventory import Inventory
from .models.productDetails import ProductDetails

from flask import Blueprint
bp = Blueprint('products', __name__)

class ExpensiveForm(FlaskForm):
    k = IntegerField('Priciest number', validators=[DataRequired(), NumberRange(min=1, max =300)])
    submit = SubmitField('sort')

class CategoryForm(FlaskForm):
    category = SelectField('Category', validators=[DataRequired()], choices=['Electronics', 'Decor', 'Grocery', 'Toys', 'Sports', 'Beauty', 'Automotive', 'Pets', 'Books', 'Movies', 'Games', 'Golf'])
    submit = SubmitField('Go')

@bp.route('/shelf', methods=['GET', 'POST'])
def shelf():
    # get all available products for sale:
    form = ExpensiveForm()
    if form.validate_on_submit():
        products = Product.get_expensive_k(True,form.k.data)
    else:
        products = Product.get_all(True)  

    categoryForm = CategoryForm()
    if categoryForm.validate_on_submit():
        products = Product.get_category(True, categoryForm.category.data)
    
    return render_template('products.html',
                           avail_products=products,
                           form=form, 
                           categoryForm=categoryForm)

@bp.route('/shelf/high2low', methods=['GET', 'POST'])
def high2low():
    # get all available products for sale:
    categoryForm = CategoryForm()
    form = ExpensiveForm()
    if form.validate_on_submit():
        products = Product.get_expensive_k(True,form.k.data)
    else:
        products = Product.get_all(True)  
    
    products = Product.get_most_expensive(True)
    
    categoryForm = CategoryForm()
    if categoryForm.validate_on_submit():
        products = Product.get_category(True, categoryForm.category.data)
    
    return render_template('products.html',
                           avail_products=products,
                           form=form, 
                           categoryForm=categoryForm)

@bp.route('/shelf/low2high', methods=['GET', 'POST'])
def low2high():
    # get all available products for sale:
    categoryForm = CategoryForm()
    form = ExpensiveForm()
    if form.validate_on_submit():
        products = Product.get_expensive_k(True,form.k.data)
    else:
        products = Product.get_all(True)  
    
    products = Product.get_least_expensive(True)
    
    categoryForm = CategoryForm()
    if categoryForm.validate_on_submit():
        products = Product.get_category(True, categoryForm.category.data)

    
    return render_template('products.html',
                           avail_products=products,
                           form=form, 
                           categoryForm=categoryForm)

@bp.route('/<int:productid>/')
def productDetails(productid=None):
    product = ProductDetails.get_details(id=productid)
    sellers = Inventory.get_by_pid(id=productid)
    return render_template('product_detailed.html', product = product, sellers=sellers)
