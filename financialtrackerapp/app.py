from flask import Flask

def create_app():
    app = Flask(__name__, template_folder= 'templates')
    app.config['DEBUG'] = True
    
    # Installing and registering the blueprints
    from financialtrackerapp.blueprints.core.routes import core
    from financialtrackerapp.blueprints.finance.routes import finance
    from financialtrackerapp.blueprints.marketplace.routes import marketplace
    
    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(finance, url_prefix='/finance')
    app.register_blueprint(marketplace, url_prefix='/marketplace')
    
    # Migrating the apps
    
    return app