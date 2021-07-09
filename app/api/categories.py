from flask import jsonify, request, current_app
from app import db
from app.api import bp
from .errors import not_found
from ..models import Category, Product, ProductCategory


@bp.route('/categories')
def category_list():
    categories = Category.query.all()

    if not categories or len(categories) == 0:
        return not_found('Category not found')

    return jsonify({'categories': [category.get_category_info() for category in categories]})


@bp.route('/categories/<id>')
def category_details(id):
    category = Category.query.filter_by(id=id).first()

    if not category:
        return not_found(f'Category with id = {id} not found')

    return jsonify(category.get_category_info())


@bp.route('/categories/<id>/products')
def category_based_product_list(id):
    category = Category.query.filter_by(id=id).first()

    if not category:
        return not_found(f'Category with id = {id} not found')

    page = request.args.get('page', 1, type=int)
    products_categories = db.session.query(ProductCategory, Product).filter(ProductCategory.category_id==category.id).join(Product, ProductCategory.product_id==Product.id).paginate(
        page, current_app.config['API_PRODUCTS_PER_PAGE'], False
    )
    next_page = page=products_categories.next_num if products_categories.has_next else None
    prev_page = page=products_categories.prev_num if products_categories.has_prev else None

    products = []
    for p_c in products_categories.items:
        products.append(p_c[1])

    return jsonify({
        'products': [product.get_product_info_minimum() for product in products],
        '_meta': {
            'page': page or 1,
            'per_page': current_app.config['API_PRODUCTS_PER_PAGE'],
            'total_pages': products_categories.pages,
            'total_items': products_categories.total,
            'next_page': next_page,
            'prev_page': prev_page
        }
    })