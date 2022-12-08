from flask import Flask
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user
import datetime
import random
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from flask_sqlalchemy import SQLAlchemy
from .models.product import Product
from .models.purchase import Purchase
from .models.purchaseDetail import PurchaseDetail
from .models.reviews import ProductReview
from .models.cart import Cart
from .models.user import User
from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('cart', __name__)
'''
class CartForm(FlaskForm):
    uid = IntegerField('User ID', validators=[DataRequired(), NumberRange(min=1, max =10000)])
    submit = SubmitField('sort')
'''
@bp.route('/items', methods=['GET', 'POST'])
def items():
    total = 0
    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
        total = 0
        for item in cart:
            total += item.subtotal
    else:
        cart = Cart.get_all()

    return render_template('cart.html',user_cart = cart, total=total)

@bp.route('/delete/<int:pid>' ,methods=['GET','POST'])
def remove(pid):
    cart = Cart.delete_item(pid)
    'cform = CartForm()'
    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
        total = 0
        for item in cart:
            total += item.subtotal
    else:
        cart = Cart.get_all()

    return render_template('cart.html', user_cart=cart, total=total)

@bp.route('/edit_num/<int:pid>' ,methods=['GET','POST'])
def edit_num(pid):
    'cform = CartForm()'
    if 'quantity' in request.form:
        quantity = request.form['quantity']
        Cart.edit_num_item(pid, quantity)
    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
        total = 0
        for item in cart:
            total += item.subtotal
    else:
        cart = Cart.get_all()

    return render_template('cart.html', user_cart=cart, total=total)

@bp.route('/submit_cart' ,methods=['GET','POST'])
def submit_cart():
    error = ''
    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
        total = 0
        currentbal = User.getvalue(current_user.id)
        for item in cart:
            total += item.subtotal
        if currentbal < total:
            error = "Insufficent Balance"
            return redirect(url_for('cart.items'))
          
        User.Updatevalue(current_user.id,value=currentbal-total)
        for item in cart:
            currentsellerbal = User.getvalue(item.sid)
            User.Updatevalue(item.sid, value=currentsellerbal+item.subtotal)
        #inventory = Inventory.editInventory()
        for item in cart:
            inventory = Inventory.get_by_pid(item.pid)
         
            old_quant = inventory[0].invNum
            new_quant = item.num_item
            if old_quant < new_quant:
                error = "Insufficent Inventory"
                return redirect(url_for('cart.items'))
            else:
                Inventory.editInventory(item.pid, value= old_quant-new_quant)
            
        Purchase.add_purchase(current_user.id)
        purchid = Purchase.get_latest_purch_id(current_user.id)
        purchase_id = purchid[0][0]
        print(purchase_id)
        
        for item in cart:
            fullfillment = bool(random.getrandbits(1))
            PurchaseDetail.add_purchasedetail(purchase_id, item.pid, item.sid, item.num_item, fullfillment)
        
        print(PurchaseDetail.get_details(purchase_id))

        
        Cart.remove_all(current_user.id)
        total = 0
        print(cart)
    return render_template('cart.html', cart=cart, total=total, error=error)
