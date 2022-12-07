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
from .models.featuredProducts import FeaturedProduct


from flask import Blueprint


bp = Blueprint('index', __name__)
class ExpensiveForm(FlaskForm):
    k = IntegerField('Priciest number', validators=[DataRequired(), NumberRange(min=1, max =300)])
    submit = SubmitField('sort')

class ReviewForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1, max =10000)])
    submit = SubmitField('sort')

class CartForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1, max =10000)])
    submit = SubmitField('sort')

class InvForm(FlaskForm):
    sid = IntegerField('User/Seller ID', validators=[DataRequired(), NumberRange(min=0, max =10000)])
    submit = SubmitField('sort')

class PurForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=0, max =10000)])
    submit = SubmitField('sort')


@bp.route('/', methods=['GET', 'POST'])
def index():
    # get all available products for sale:
    featured = FeaturedProduct.get_featured()

    # render the page by adding information to the index.html file
    return render_template('index.html', 
                           featured=featured)
