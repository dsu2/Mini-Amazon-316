from flask import Flask
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_sqlalchemy import SQLAlchemy
import datetime
from .models.product import Product
from .models.purchase import Purchase
from .models.reviews import ProductReview
from .models.cart import Cart
from .models.inventory import Inventory, Order_fulfillment

from flask import Blueprint
bp = Blueprint('inventory', __name__)

class InvForm(FlaskForm):
    sid = IntegerField('User/Seller ID', validators=[DataRequired(), NumberRange(min=0, max =10000)])
    submit = SubmitField('sort')

@bp.route('/prod', methods=['GET', 'POST'])
def prod():
    seller_id = Inventory.get_seller_id(current_user.id)[0][0]
    if current_user.is_authenticated:
        inv = Inventory.get_by_sid(seller_id)
        ord = Order_fulfillment.get_orders(seller_id)
    else:
        inv = Inventory.get_all()
        ord = Order_fulfillment.get_orders(0)

    return render_template('inventory.html',user_inventory = inv, orders = ord)

@bp.route('/delete_inv/<int:pid>' ,methods=['GET','POST'])
def remove(pid):
    seller_id = Inventory.get_seller_id(current_user.id)[0][0]
    inv = Inventory.delete(pid, seller_id)
    if current_user.is_authenticated:
        ord = Order_fulfillment.get_orders(seller_id)
        inv = Inventory.get_by_sid(seller_id)
    else:
        inv = Inventory.get_all()
        ord = Order_fulfillment.get_orders(0)

    return render_template('inventory.html', user_inventory = inv, orders = ord)

@bp.route('/edit_num_inv/<int:pid>/<int:sid>' ,methods=['GET','POST'])
def edit_num(pid, sid):
    seller_id = Inventory.get_seller_id(current_user.id)[0][0]
    if 'quantity' in request.form:
        quantity = request.form['quantity']
        Inventory.edit_num_item(pid, sid, quantity)
    if current_user.is_authenticated:
        ord = Order_fulfillment.get_orders(seller_id)
        inv = Inventory.get_by_sid(seller_id)
    else:
        inv = Inventory.get_all()
        ord = Order_fulfillment.get_orders(0)

    return render_template('inventory.html', user_inventory=inv, orders = ord)


@bp.route('/add_inv/<int:sid>' ,methods=['GET','POST'])
def add_inv(sid):
    seller_id = Inventory.get_seller_id(current_user.id)[0][0]
    if 'prod_id' in request.form:
        pid = request.form['prod_id']
        Inventory.addInventory(seller_id, pid, 1)
    if current_user.is_authenticated:
        ord = Order_fulfillment.get_orders(seller_id)
        inv = Inventory.get_by_sid(seller_id)
    else:
        inv = Inventory.get_all()
        ord = Order_fulfillment.get_orders(0)

    return render_template('inventory.html', user_inventory=inv, orders = ord)


@bp.route('/mark_fulfilled/<int:purch_id>' ,methods=['GET','POST'])
def mark_fulfilled(purch_id):
    Order_fulfillment.mark_fulfilled(purch_id)
    seller_id = Inventory.get_seller_id(current_user.id)[0][0]
    if current_user.is_authenticated:
        ord = Order_fulfillment.get_orders(seller_id)
        inv = Inventory.get_by_sid(seller_id)
    else:
        inv = Inventory.get_all()
        ord = Order_fulfillment.get_orders(0)

    return render_template('inventory.html', user_inventory = inv, orders = ord)