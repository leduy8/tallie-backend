from flask import jsonify, request, current_app
from app import db
from app.api import bp
from .errors import bad_request, not_found
from ..models import Product, User, Seen
from ..middlewares import token_required


@bp.route('/seen', methods=['GET'])
@token_required
def seen_products(decoded):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    page = request.args.get('page', 1, type=int)
    seen_products = db.session.query(Seen, Product).filter(Seen.user_id==user.id).join(Product, Seen.product_id==Product.id).paginate(
        page, current_app.config['API_PRODUCTS_PER_PAGE'], False
    )
    next_page = page=seen_products.next_num if seen_products.has_next else None
    prev_page = page=seen_products.prev_num if seen_products.has_prev else None

    products = []
    for w_p in seen_products.items:
        products.append(w_p[1])

    return jsonify({
        'products': [product.get_product_info_minimum() for product in products],
        '_meta': {
            'page': page or 1,
            'per_page': current_app.config['API_PRODUCTS_PER_PAGE'],
            'total_pages': seen_products.pages,
            'total_items': seen_products.total,
            'next_page': next_page,
            'prev_page': prev_page
        }
    })
    

@bp.route('/seen', methods=['POST'])
@token_required
def add_to_seen(decoded):
    user = User.query.filter_by(id=decoded['id']).first()
    data = request.get_json()

    if not user:
        return not_found('User\'s not found')

    if 'product_id' not in data:
        return bad_request('Product id is not found')

    if type(data['product_id']) is not int:
        return bad_request('Product id is not in right data type')

    product = Product.query.filter_by(id=data['product_id']).first()
    
    if not product:
        return bad_request('Invalid product id')

    user.seen.append(product)
    db.session.add(user)
    db.session.commit()

    return jsonify('Added to seen'), 201