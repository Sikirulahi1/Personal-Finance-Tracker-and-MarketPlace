from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from financialtrackerapp.app import bcrypt, db, oauth
from financialtrackerapp.blueprints.core.models import User
from flask_login import login_user, logout_user, current_user, login_required


core = Blueprint('core', __name__, template_folder = 'templates')


@core.route('/')
@login_required
def index():
    return render_template('finance/index.html')

@core.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('core/signup.html')
    
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('The email has already been used', 'danger')
            return redirect(url_for('core.signup'))
        
        # Hash the password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create and save new user
        new_user = User(
            username=username, 
            password=password_hash, 
            email=email, 
            balance=float(0.0), 
            savings=float(0.0), 
            budget=float(0.0)
            )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('core.login'))
    
    
@core.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('core/login.html')
    
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            flash('Successfully logged in', 'success')
            
            login_user(user)
            return redirect(url_for('finance.index'))
        elif user and user.google_id and not user.password:
            # If account exists with Google but no password set
            flash('Please use Google Login for this account.', 'warning')
            return redirect(url_for('core.login'))
        else:
            flash('Incorrect Email or Password', 'danger')
            return redirect(url_for('core.login'))



# The google login format
@core.route('/google_login')
def google_login():
    redirect_uri = url_for('core.authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


# To authorize google login
@core.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.get('userinfo').json()
    
    # Check if a user exists with this email
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        # New user, create an entry with Google details
        user = User(
            username=user_info['given_name'],
            email=user_info['email'],
            google_id=user_info['id'],
            balance=float(0.0),
            savings=float(0.0),
            budget=float(0.0)
        )
        db.session.add(user)
        db.session.commit()
    
    elif not user.google_id:
        # Existing email-based user, update with Google ID
        user.google_id = user_info['id']
        db.session.commit()
    
    # Log the user in
    login_user(user)
    flash('Logged in successfully with Google', 'success')
    return redirect(url_for('finance.index'))

@core.route('/logout')
def logout():
    logout_user() 
    flash('You have been logged out.', 'success')
    return redirect(url_for('core.login'))  
    
        
        
        
        