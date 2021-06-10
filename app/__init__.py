from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
mail = Mail(app)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.orders import bp as orders_bp
app.register_blueprint(orders_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from app import routes, models