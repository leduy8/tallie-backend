from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from elasticsearch import Elasticsearch
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
    
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.orders import bp as orders_bp
    app.register_blueprint(orders_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    from app.products import bp as products_bp
    app.register_blueprint(products_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models, email