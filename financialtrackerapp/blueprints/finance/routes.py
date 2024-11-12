from flask import Flask, Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from financialtrackerapp.app import db
from financialtrackerapp.blueprints.finance.models import Transaction

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
        description = request.form.get('description')
        transaction = Transaction(
            user_id=current_user.uid,
            total_amount=deposit_amount,
            transaction_type='Deposit',
            description = description,
            status='Pending'
        )
        db.session.add(transaction)
        db.session.commit()
        
        if deposit_amount and deposit_amount > 0:
            current_user.balance += deposit_amount
            flash(f"Deposited ${deposit_amount:.2f} successfully!", 'success')
            
        transaction.status = 'Completed'
        db.session.commit()
        return redirect(url_for('finance.index'))
    
    return render_template('finance/deposit.html')


@finance.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        withdraw_amount = is_valid_amount(request.form.get('withdraw'))
        description = request.form.get('description')
        transaction = Transaction(
            user_id=current_user.uid,
            total_amount=withdraw_amount,
            transaction_type='Withdraw',
            description = description,
            status='Pending'
        )
        db.session.add(transaction)
        db.session.commit()
        
        if withdraw_amount:
            if current_user.balance >= withdraw_amount:
                current_user.balance -= withdraw_amount
                flash(f"Successfully withdrawn ${withdraw_amount:.2f}", 'success')
            else:
                transaction.status = 'Failed'
                db.session.commit()
                db.session.rollback()
                flash("Insufficient balance for this withdrawal.", 'danger')
                return redirect(url_for('finance.withdraw'))
                
        transaction.status = 'Completed'
        db.session.commit()
        return redirect(url_for('finance.index'))
    
    return render_template('finance/withdraw.html')


@finance.route('/save_money', methods=['GET', 'POST'])
@login_required
def save_money():
    if request.method == 'POST':
        savings_amount = is_valid_amount(request.form.get('save_money'))
        description = request.form.get('description')
        transaction = Transaction(
            user_id=current_user.uid,
            total_amount=savings_amount,
            transaction_type='Deposit into Savings',
            description = description,
            status='Pending'
        )
        db.session.add(transaction)
        db.session.commit()
        
        if savings_amount:
            if current_user.balance >= savings_amount:
                current_user.savings += savings_amount
                current_user.balance -= savings_amount
                flash(f"Successfully saved ${savings_amount:.2f} to savings.", 'success')
            else:
                transaction.status = 'Failed'
                db.session.commit()
                db.session.rollback()
                flash("Insufficient balance to save this amount.", 'danger')
                return redirect(url_for('finance.save_money'))
                
        transaction.status = 'Completed'
        db.session.commit()
        return redirect(url_for('finance.index'))
    
    return render_template('finance/saveMoney.html')


@finance.route('/withdraw_from_savings', methods=['GET', 'POST'])
@login_required
def withdraw_from_savings():
    if request.method == 'POST':
        amount = is_valid_amount(request.form.get('withdraw'))
        description = request.form.get('description')
        transaction = Transaction(
            user_id=current_user.uid,
            total_amount=amount,
            transaction_type='Withdraw from Savings',
            description = description,
            status='Pending'
        )
        db.session.add(transaction)
        db.session.commit()
        
        if amount:
            if current_user.savings >= amount:
                current_user.savings -= amount
                current_user.balance += amount

                flash(f"Successfully withdrawn ${amount:.2f} from savings.", 'success')
            else:
                transaction.status = 'Failed'
                db.session.commit()
                db.session.rollback()
                flash("Insufficient savings for this withdrawal.", 'danger')
                return redirect(url_for('finance.withdraw_from_savings'))
        transaction.status = 'Completed'
        db.session.commit()
        return redirect(url_for('finance.index'))
    
    return render_template('finance/savingsWithdraw.html')

@finance.route('/transaction_history')
@login_required
def transaction_history():
    transactions = Transaction.query.filter_by(user_id=current_user.uid).order_by(Transaction.date.desc()).all()
    return render_template('finance/transaction_history.html', transactions=transactions)

@finance.route('/back_from_history')
@login_required
def back_from_history():
    return redirect(url_for('finance.index'))