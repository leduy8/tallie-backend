from time import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import URLType
from flask_login import UserMixin
import jwt
from app import app, db


class Payment(db.Model):
    card_number = db.Column(db.String(14), primary_key=True)
    credentials = db.Column(db.String(8000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def validate(cls):
        pass

    def __repr__(self) -> str:
        return f'<Payment {self.card_number} owned by user with id: {self.user_id}>'


class Wishlist(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

    def __repr__(self) -> str:
        return f'<Wishlist owned by user with id: {self.user_id}>'


class Seen(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Seen lastseen={self.timestamp} by user with id: {self.user_id}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50), index=True, unique=True)
    email_activated = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(10))
    address = db.Column(db.String(150))
    bio = db.Column(db.String(250))
    is_seller = db.Column(db.Boolean, default=False)
    products = db.relationship('Product', backref='seller', lazy='dynamic')
    payment = db.relationship('Payment', lazy='dynamic')
    wishlist = db.relationship(
        'Product',
        secondary='wishlist',
        lazy='dynamic'
    )
    seen = db.relationship(
        'Product',
        secondary='seen',
        lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_generate_token(self, expires_in=600):
        print(jwt.encode({'generated_token': self.id, 'exp': time() + expires_in},app.config['SECRET_KEY'], algorithm='HS256'))
        return jwt.encode({'generated_token': self.id, 'exp': time() + expires_in},app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_generated_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['generated_token']
        except:
            return
        return User.query.get(id)
    
    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(URLType)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self) -> str:
        return f'<Picture {self.url}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self) -> str:
        return f'<Category {self.name}>'


class ProductCategory(db.Model):
    __tablename__ = 'productcategory'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    author = db.Column(db.String(100), index=True)
    price = db.Column(db.Float(precision=2))
    description = db.Column(db.String(2000))
    quantity = db.Column(db.Integer)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pictures = db.relationship('Picture', lazy='dynamic')
    categories = db.relationship(
        'Category', 
        secondary='productcategory',
        lazy='dynamic'
    )

    def __repr__(self) -> str:
        return f'<Product {self.name}>'


class Abuse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))

    def __repr__(self) -> str:
        return f'<Abuse {self.id}>'


class Helpful(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))

    def __repr__(self) -> str:
        return f'<Helpful {self.id}>'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    star = db.Column(db.Integer)
    overview = db.Column(db.String(50))
    content = db.Column(db.String(150))
    prevent_spoiler = db.Column(db.Boolean, default=False)
    started_reading = db.Column(db.DateTime, nullable=True)
    finished_reading = db.Column(db.DateTime, nullable=True)
    abuses = db.relationship('Abuse', lazy='dynamic')
    helpfuls = db.relationship('Helpful', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Review {self.id}, {self.content}>'
