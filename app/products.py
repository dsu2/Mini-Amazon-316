from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
import datetime
import sys
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, AnyOf, Length, URL

from .models.product import Product
from .models.purchase import Purchase
from .models.reviews import ProductReview
from .models.cart import Cart
from .models.inventory import Inventory
from .models.productDetails import ProductDetails
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('products', __name__)

class ExpensiveForm(FlaskForm):
    k = IntegerField('Priciest number', validators=[DataRequired(), NumberRange(min=1, max =300)])
    submit = SubmitField('sort')

class CategoryForm(FlaskForm):
    category = SelectField('Category', validators=[DataRequired()], choices=['Electronics', 'Decor', 'Grocery', 'Toys', 'Sports', 'Beauty', 'Automotive', 'Pets', 'Books', 'Movies', 'Games', 'Golf'])
    submit = SubmitField('Go')

class SearchForm(FlaskForm):
    search = StringField('Search products by name', validators=[DataRequired(), Length(min=1, max=150)])
    submit = SubmitField('Search')


class ReviewForm(FlaskForm):
    text = StringField('Text for review', validators = [DataRequired()])
    val = IntegerField('Rating from 1-10', validators=[DataRequired(), NumberRange(min=1, max =10)])
    submit = SubmitField('Add Review')

class EditForm(FlaskForm):
    text = StringField('New text for updated review', validators = [DataRequired()])
    val = IntegerField('New rating from 1-10', validators=[DataRequired(), NumberRange(min=1, max =10)])
    submit = SubmitField('Edit Review')

class RemoveForm(FlaskForm):
    submit = SubmitField('Remove Review')

class NewProductForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired(), Length(min=2, max=1000)])
    price = DecimalField("Price", places=2, validators=[DataRequired(), NumberRange(min=.01, max = 1000000)])   
    category = SelectField("Category", validators=[DataRequired()], choices=['Electronics', 'Decor', 'Grocery', 'Toys', 'Sports', 'Beauty', 'Automotive', 'Pets', 'Books', 'Movies', 'Games', 'Golf'])
    des = StringField("Description", validators = [DataRequired(), Length(min=10, max=10000)])
    image = StringField("Image URL", validators=[DataRequired(), URL()])
    inventoryNum = IntegerField("Amount of product", validators=[DataRequired(), NumberRange(min=0, max = 100000)])
    submit = SubmitField('Post product')


@bp.route('/shelf', methods=['GET', 'POST'])
def shelf():
    
   
   
    form = ExpensiveForm()
    products = Product.get_all(True)
    if form.validate_on_submit():
        top_x = form.k.data
        products = Product.get_expensive_k(True,form.k.data)
    else:
        top_x = None
        

    categoryForm = CategoryForm()
    if categoryForm.validate_on_submit():
        category = categoryForm.category.data
        products = Product.get_category(True, categoryForm.category.data)
    else:
        category = None

    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        search_data = searchForm.search.data
        products = Product.get_search(True, searchForm.search.data)
    else: 
        search_data = None

    '''products = Product.get_product_list(top_x, category, search_data)'''
    
    return render_template('products.html',
                           avail_products=products,
                           form=form, 
                           categoryForm=categoryForm,
                           searchForm=searchForm)

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

    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        products = Product.get_search(True, searchForm.search.data)
    
    return render_template('products.html',
                           avail_products=products,
                           form=form, 
                           categoryForm=categoryForm,
                           searchForm=searchForm)

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

    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        products = Product.get_search(True, searchForm.search.data)

    
    return render_template('products.html',
                           avail_products=products,
                           form=form, 
                           categoryForm=categoryForm,
                           searchForm=searchForm)

@bp.route('/pid/<int:productid>/', methods=['GET', 'POST'])
def productDetails(productid=None):

    sellers = Inventory.get_by_pid(id=productid)
    product = ProductDetails.get_details(id=productid)
    reviews = ProductReview.get_all_by_pid(productid)
    avgreview = ProductReview.findAvgRating(pid=productid)
    numreview = ProductReview.findNumReview(pid=productid)

    print(avgreview, file=sys.stdout)
    print(numreview, file=sys.stdout)

    if avgreview==None:
        avgreview = None
    else:
        avgreview = round(avgreview, 3)


    form = ReviewForm()
    if form.validate_on_submit():
        if current_user.get_id() != None:
            ProductReview.addProductReview(pid = productid, uid = current_user.get_id(), text = form.text.data, rating = form.val.data)  
            reviews = ProductReview.get_all_by_pid(productid)
    return render_template('product_detailed.html', product= product, sellers=sellers, reviews = reviews, form = form, pid = productid, avgreview = avgreview, numreview =numreview)

 
@bp.route('/pid/<int:productid>/editreview/', methods=['GET', 'POST'])
def editReview(productid = None):
    sellers = Inventory.get_by_pid(id=productid)
    product = ProductDetails.get_details(id=productid)
    form = ReviewForm()

    userid = current_user.get_id()
    editform = EditForm()
    removeform = RemoveForm()
    if editform.validate_on_submit():
        print('edit Form is Valid', file=sys.stdout)
        ProductReview.editProductReview(pid = productid, uid = userid, text = editform.text.data, rating = editform.val.data)
        reviews = ProductReview.get_all_by_pid(productid)
        avgreview = ProductReview.findAvgRating(pid=productid)
        numreview = ProductReview.findNumReview(pid=productid)

        print(avgreview, file=sys.stdout)
        print(numreview, file=sys.stdout)

        if avgreview==None:
            avgreview = None
        else:
            avgreview = round(avgreview, 3)

        return render_template('product_detailed.html', product= product, sellers=sellers, reviews = reviews, form = form, pid = productid,avgreview = avgreview, numreview =numreview)

   
    if removeform.validate_on_submit():
        print('Remove form is Valid', file=sys.stdout)
        ProductReview.removeProductReview(pid = productid, uid = userid)
        reviews = ProductReview.get_all_by_pid(productid)
        avgreview = ProductReview.findAvgRating(pid=productid)
        numreview = ProductReview.findNumReview(pid=productid)

        print(avgreview, file=sys.stdout)
        print(numreview, file=sys.stdout)

        if avgreview==None:
            avgreview = None
        else:
            avgreview = round(avgreview, 3)
         
        return render_template('product_detailed.html', product = product, sellers=sellers, reviews = reviews, form = form, pid = productid,avgreview = avgreview, numreview =numreview)

    return render_template('edit_review.html', editform = editform, removeform = removeform, productid = productid)

@bp.route('/shelf/addProduct', methods=['GET', 'POST'])
def addProduct():
    userid = current_user.get_id()
    sid = Seller.get_sid(current_user.id)

    newForm = NewProductForm()
    if newForm.validate_on_submit():
        new_pid = ProductDetails.addProduct(newForm.name.data, newForm.price.data, newForm.category.data, True, newForm.des.data, newForm.image.data)
        if new_pid:
            Inventory.addInventory(sid, new_pid, newForm.inventoryNum.data)

    if sid is None:
        return render_template('sellerSignUp.html')
    else:
        return render_template('postProduct.html', newForm=newForm)
