from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from app import db


class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def validate(cls):
        pass

    def __repr__(self) -> str:
        return f'<Shipping>'


class Payment(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    credentials = db.Column(db.String(8000))

    @classmethod
    def validate(cls):
        pass

    def __repr__(self) -> str:
        return f'<Payment {self.card_number}'


class Wishlist(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

    def __repr__(self) -> str:
        return f'<Wishlist>'


class Seen(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'<Seen lastseen={self.timestamp}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50), index=True, unique=True)
    phone = db.Column(db.String(10))
    address = db.Column(db.String(150))
    bio = db.Column(db.String(250))
    is_seller = db.Column(db.Boolean())
    products = db.relationship('Product', backref='seller', lazy='dynamic')
    payment = db.relationship('Shipping', lazy='dynamic')
    shipping = db.relationship('Payment', lazy='dynamic')
    wishlist = db.relationship(
        'User',
        secondary='wishlist',
        lazy='dynamic'
    )
    seen = db.relationship(
        'User',
        secondary='seen',
        lazy='dynamic'
    )
    reviews = db.relationship('Review', lazy='dynamic')
    orders = db.relationship('Order', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(URLType)

    def __repr__(self) -> str:
        return f'<Picture {self.url}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)

    def __repr__(self) -> str:
        return f'<Category {self.name}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    price = db.Column(db.Float(precision=2))
    description = db.Column(db.String(80))
    quantity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pictures = db.relationship('Picture', backref='product', lazy='dynamic')
    categories = db.relationship('Category', backref='product', lazy='dynamic')
    reviews = db.relationship('Review', lazy='dynamic')
    shipping_id = db.Column(db.Integer, db.ForeignKey('shipping.id'))

    def __repr__(self) -> str:
        return f'<Product {self.name}>'


class Order(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deliver_to = db.Column(db.String(150))
    has_taken = db.Column(db.Boolean, default=False)
    is_delivering = db.Column(db.Boolean, default=False)
    is_delivered = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f'<Order {self.user_id}${self.product_id}>'


class Abuse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))


class Helpful(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    star = db.Column(db.Integer)
    overview = db.Column(db.String(50))
    content = db.Column(db.String(150))
    prevent_spoiler = db.Column(db.Boolean)
    started_reading = db.Column(db.DateTime, nullable=False)
    finished_reading = db.Column(db.DateTime, nullable=False)
    abuses = db.relationship('Abuse', lazy='dynamic')
    helpfuls = db.relationship('Helpful', lazy='dynamic')
