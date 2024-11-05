from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder= 'templates')
    bcrypt = Bcrypt(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./fintech.db'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mygooodlord@5432/fintech'
    app.config['DEBUG'] = True
    app.secret_key = 'd29fcc6206dab14e152635ce67605e05'
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
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