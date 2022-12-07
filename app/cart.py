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
    if current_user.is_authenticated:
        cart = Cart.get_cart(current_user.id)
        total = 0
        currentbal = User.getvalue(current_user.id)
        for item in cart:
            total += item.subtotal
        if currentbal < total:
            flash('insufficent balance!')
            return redirect(url_for('cart.items'))
          
        User.Updatevalue(current_user.id,value=currentbal-total)
        for item in cart:
            currentsellerbal = User.getvalue(item.sid)
            User.Updatevalue(item.sid, value=currentsellerbal+item.subtotal)
        #inventory = Inventory.editInventory()
        for item in cart:
            inventory = Inventory.get_by_pid(item.pid)
            print(inventory[0])
            old_quant = inventory[0].invNum
            new_quant = item.num_item
            if old_quant < new_quant:
                Inventory.editInventory(item.pid, value= 0)
            else:
                Inventory.editInventory(item.pid, value= old_quant-new_quant)
            
            Purchase.add_purchase(current_user.id, inventory[0].pid, inventory[0].sid)
            'purchaseele = Purchase.get_by_purchaseid()'
            'PurchaseDetail.add_purchasedetail(purchaseele, item.subtotal,item.num_item)'
        'Purchase.add_purchase(current_user.id, inventory[0].pid, inventory[0].sid)'
        cart = Cart.remove_all(current_user.id)
    return render_template('cart.html', cart=cart, total=total)
