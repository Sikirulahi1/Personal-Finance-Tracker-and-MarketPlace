from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required, current_user
from financialtrackerapp.app import db
from financialtrackerapp.blueprints.marketplace.models import Product
from financialtrackerapp.blueprints.marketplace.models import CartItem

marketplace = Blueprint('marketplace', __name__, template_folder = 'templates')

@marketplace.route('/')
@login_required
def index():
    # Fetch all the products from the database
    products = Product.query.all()
    return render_template('marketplace/index.html', products=products)


@marketplace.route('/add_to_cart', methods=['GET', 'POST'])
@login_required
def add_to_cart():
    product_id = request.form.get('product_id')
    product_name = request.form.get('product_name')
    product_price = float(request.form.get('product_price'))
    product_quantity = int(request.form.get('product_quantity'))
    
    user_id = current_user.uid
    
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += product_quantity
    else:
        new_item = CartItem(
            product_id = product_id,
            user_id = user_id,
            product_name = product_name,
            price = product_price,
            quantity = product_quantity
        )
        db.session.add(new_item)
        
    db.session.commit()
    
    return redirect(url_for('marketplace.index'))
    
    
@marketplace.route('/cart_items')
@login_required
def cart_items():
    user_id = current_user.uid
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    total_amount = round(sum([cart_item.quantity * cart_item.price for cart_item in cart_items]), 2)
    return render_template('marketplace/cart.html', cart_items=cart_items, total_amount=total_amount)
    
@marketplace.route('/delete_from_cart/<int:product_id>', methods = ['POST'])
@login_required
def delete_from_cart(product_id):
    user_id = current_user.uid
    item_to_delete = CartItem.query.filter_by(product_id=product_id, user_id=user_id).first()
    
    if item_to_delete:
        db.session.delete(item_to_delete)
        db.session.commit()
        
    return redirect(url_for('marketplace.cart_items'))


@marketplace.route('/clear_cart', methods=['POST'])
@login_required
def clear_cart():
    CartItem.query.filter_by(user_id=current_user.uid).delete()

    db.session.commit()
    return redirect(url_for('marketplace.cart_items'))

@marketplace.route('/proceed_to_checkout')
def proceed_to_checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.uid).all()
    total_amount = round(sum([cart_item.quantity * cart_item.price for cart_item in cart_items]), 2)
    return render_template('marketplace/proceed_to_checkout.html', cart_items=cart_items, total_amount=total_amount)
    

@marketplace.route('/make_payment', methods=['POST'])
def make_payment():
    total_amount = request.form.get('total_amount')
    if total_amount:
        current_user.balance -= float(total_amount)
        CartItem.query.filter_by(user_id=current_user.uid).delete()
        
    db.session.commit()
    return redirect(url_for('finance.index'))