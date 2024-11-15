from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
oauth = OAuth()

def create_app():
    app = Flask(__name__, template_folder= 'templates')
    bcrypt = Bcrypt(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./fintech.db'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mygooodlord@5432/fintech'
    app.config['DEBUG'] = True
    app.secret_key = os.getenv('SECRET_KEY')
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)
    
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'openid email profile'},
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )
    
    from financialtrackerapp.blueprints.core.models import User
    
    @login_manager.user_loader
    def user_loader(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('core.login'))
    
    # Installing and registering the blueprints
    from financialtrackerapp.blueprints.core.routes import core
    from financialtrackerapp.blueprints.finance.routes import finance
    from financialtrackerapp.blueprints.marketplace.routes import marketplace
    
    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(finance, url_prefix='/finance')
    app.register_blueprint(marketplace, url_prefix='/marketplace')
    
    # Migrating the apps
    migrate = Migrate(app, db)
    
    return app