from flask import jsonify, request
from app.api import bp
from .errors import bad_request, not_found
from ..models import Product


@bp.route('/products/featured')
def featured_products():
    pass


@bp.route('/products/best_selling_this_month')
def best_selling_products():
    pass


@bp.route('/products/most_viewed')
def most_viewed_products():
    pass


@bp.route('/products/search')
def searched_products():
    pass


@bp.route('/products/<id>')
def get_product_detail(id):
    product = Product.query.filter_by(id=id).first()

    if not product:
        return not_found('Product\'s not found')

    return jsonify(product.get_product_info())


@bp.route('/products/<id>/validate')
def product_validation(id):
    product = Product.query.filter_by(id=id).first()

    if not product:
        return not_found('Product\'s not found')

    return jsonify({'is_validated': True})