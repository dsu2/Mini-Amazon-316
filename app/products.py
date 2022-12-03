from flask import render_template, redirect, url_for, flash, request
from flask_paginate import Pagination, get_page_parameter, get_page_args
from werkzeug.urls import url_parse
from flask_login import current_user
import datetime
import sys
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DecimalField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, AnyOf, Length, URL, Optional


from .models.product import Product
from .models.purchase import Purchase
from .models.reviews import ProductReview
from .models.cart import Cart
from .models.inventory import Inventory
from .models.productDetails import ProductDetails
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('products', __name__)

class SearchForm(FlaskForm):
    k = IntegerField('Number of products', validators=[Optional(), NumberRange(min=1, max =1000)])
    category = SelectField('Category', validators=[Optional()], choices=['All Categories','Electronics', 'Decor', 'Grocery', 'Toys', 'Sports', 'Beauty', 'Automotive', 'Pets', 'Books', 'Movies', 'Games', 'Golf'])
    search = StringField('Search products by name', validators=[Optional(), Length(min=1, max=150)])
    byPrice = SelectField('Sort by Price', validators=[Optional()], choices=['None', 'LowtoHigh', 'HightoLow'])
    submit = SubmitField('Search')

class PageForm(FlaskForm):
    pageNum = IntegerField('Page number:', validators=[Optional(), NumberRange(min=1, max=1000)])
    perPage = IntegerField('Products per page:', validators=[Optional(), NumberRange(min=1, max =100)])
    submit = SubmitField("Go")
    

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
    submit = SubmitField('Post new product')

class OldForm(FlaskForm):
    name2 = StringField("Name", validators = [DataRequired(), Length(min=2, max=1000)])
    inventoryNum2 = IntegerField("Amount", validators=[DataRequired(), NumberRange(min=0, max = 100000)])
    submit2 = SubmitField('List product', validators=[DataRequired()])

class AddToCartForm(FlaskForm):
    sid = HiddenField()
    submit = SubmitField('Add To Cart')


@bp.route('/shelf', methods=['GET', 'POST'])
def shelf():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page=50

    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('products.shelf', available='True', number=form.k.data, category=form.category.data, search=form.search.data, byPrice=form.byPrice.data))
        
    number = request.args.get('number','')
    category = request.args.get('category','')
    search = request.args.get('search','')
    byPrice = request.args.get('byPrice','')

    products = Product.get_product_list(True, number, category, search, byPrice)    
    pagination_products = products[offset:offset+per_page]

    pagination = Pagination(page=page, total=len(products), record_name='products', per_page=per_page)
    
    return render_template('products.html',
                           avail_products=pagination_products,
                           form=form, pagination=pagination, page=page, per_page=per_page)

@bp.route('/pid/<int:productid>/', methods=['GET', 'POST'])
def productDetails(productid=None, sellerid=None):
    error=''
    sellerid = request.args.get('sellerid','')
    print(productid, file=sys.stdout)
    print(sellerid, file=sys.stdout)
   
    if sellerid !="":
        myUID = Cart.addToCart(current_user.id, productid, sellerid, 1)
        if myUID is None:
            error = "Already in cart! Adjust quantity in cart."
        else:
            error = "Success! Added to cart"

    
    sellers = Inventory.get_by_pid(productid)
    product = ProductDetails.get_details(id=productid)
    reviews = ProductReview.get_all_by_pid(productid)
    avgreview = ProductReview.findAvgRating(pid=productid)
    numreview = ProductReview.findNumReview(pid=productid)
    
    

    if avgreview==None:
        avgreview = None
    else:
        avgreview = round(avgreview, 3)


    form = ReviewForm()
    if form.validate_on_submit():
        if current_user.get_id() != None:
            ProductReview.addProductReview(pid = productid, uid = current_user.get_id(), text = form.text.data, rating = form.val.data)  
            reviews = ProductReview.get_all_by_pid(productid)
    
    
       

    return render_template('product_detailed.html', product= product, sellers=sellers, reviews = reviews, form = form, pid = productid, avgreview = avgreview, numreview =numreview, error=error)

 
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
    error=""
    
    newForm = NewProductForm()
    oldForm2 = OldForm()
    if newForm.validate_on_submit():
        new_pid = ProductDetails.addProduct(newForm.name.data, newForm.price.data, newForm.category.data, True, newForm.des.data, newForm.image.data)
        if new_pid: 
            Inventory.addInventory(sid, new_pid, newForm.inventoryNum.data)
            error = "Success! Product added"
        else:
            error = "Product already exists! Use 'Sell existing product' instead"
    
    
    if oldForm2.validate_on_submit():
        old_pid = Product.get_by_name(oldForm2.name2.data)
        print("How am I here now? especially", file=sys.stdout)
        if old_pid is not None:
            pid = Inventory.addInventory(sid, old_pid, oldForm2.inventoryNum2.data)
            if pid:
                error = "Success! Product added"
            else:
                error = "Product is already listed by you. Check listings"
        else:
            error = "Product does not exist! Use 'New Product' instead"

    if sid is None:
        return render_template('sellerSignUp.html')
    else:
        return render_template('postProduct.html', newForm=newForm, oldForm=oldForm2, error=error)

