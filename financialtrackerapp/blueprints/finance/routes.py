from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from financialtrackerapp.app import db

finance = Blueprint('finance', __name__, template_folder='templates')

def is_valid_amount(amount):
    """Helper function to check if the amount is a valid positive number."""
    try:
        amount = float(amount)
        if amount > 0:
            return amount
        else:
            flash("Amount must be a positive number.", 'danger')
    except (ValueError, TypeError):
        flash("Invalid amount. Please enter a numeric value.", 'danger')
    return None

@finance.route('/')
def index():
    return render_template('finance/index.html')


@finance.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'POST':
        deposit_amount = is_valid_amount(request.form.get('deposit'))
        
        if deposit_amount:
            current_user.balance += deposit_amount
            db.session.commit()
            flash(f"Deposited ${deposit_amount:.2f} successfully!", 'success')
        return redirect(url_for('finance.index'))
    
    return render_template('finance/deposit.html')


@finance.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        withdraw_amount = is_valid_amount(request.form.get('withdraw'))
        
        if withdraw_amount:
            if current_user.balance >= withdraw_amount:
                current_user.balance -= withdraw_amount
                db.session.commit()
                flash(f"Successfully withdrawn ${withdraw_amount:.2f}", 'success')
            else:
                flash("Insufficient balance for this withdrawal.", 'danger')
        return redirect(url_for('finance.index'))
    
    return render_template('finance/withdraw.html')


@finance.route('/save_money', methods=['GET', 'POST'])
@login_required
def save_money():
    if request.method == 'POST':
        savings_amount = is_valid_amount(request.form.get('save_money'))
        
        if savings_amount:
            if current_user.balance >= savings_amount:
                current_user.savings += savings_amount
                current_user.balance -= savings_amount
                db.session.commit()
                flash(f"Successfully saved ${savings_amount:.2f} to savings.", 'success')
            else:
                flash("Insufficient balance to save this amount.", 'danger')
        return redirect(url_for('finance.index'))
    
    return render_template('finance/saveMoney.html')


@finance.route('/withdraw_from_savings', methods=['GET', 'POST'])
@login_required
def withdraw_from_savings():
    if request.method == 'POST':
        amount = is_valid_amount(request.form.get('withdraw'))
        
        if amount:
            if current_user.savings >= amount:
                current_user.savings -= amount
                current_user.balance += amount
                db.session.commit()
                flash(f"Successfully withdrawn ${amount:.2f} from savings.", 'success')
            else:
                flash("Insufficient savings for this withdrawal.", 'danger')
        return redirect(url_for('finance.index'))
    
    return render_template('finance/savingsWithdraw.html')
