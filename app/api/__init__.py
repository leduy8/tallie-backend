from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import errors, auth, users, products, categories, wishlist, seen, review