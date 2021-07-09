from flask import jsonify, request, current_app
from app import db
from app.api import bp
from .errors import bad_request, not_found
from ..models import Product, User, Wishlist
from ..middlewares import token_required


@bp.route('/wishlist', methods=['GET'])
@token_required
def wishlist_products(decoded):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    page = request.args.get('page', 1, type=int)
    wishlist_products = db.session.query(Wishlist, Product).filter(Wishlist.user_id==user.id).join(Product, Wishlist.product_id==Product.id).paginate(
        page, current_app.config['API_PRODUCTS_PER_PAGE'], False
    )
    next_page = page=wishlist_products.next_num if wishlist_products.has_next else None
    prev_page = page=wishlist_products.prev_num if wishlist_products.has_prev else None

    products = []
    for w_p in wishlist_products.items:
        products.append(w_p[1])

    return jsonify({
        'products': [product.get_product_info_minimum() for product in products],
        '_meta': {
            'page': page or 1,
            'per_page': current_app.config['API_PRODUCTS_PER_PAGE'],
            'total_pages': wishlist_products.pages,
            'total_items': wishlist_products.total,
            'next_page': next_page,
            'prev_page': prev_page
        }
    })
    

@bp.route('/wishlist', methods=['POST'])
@token_required
def add_to_wishlist(decoded):
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

    user.wishlist.append(product)
    db.session.add(user)
    db.session.commit()

    return jsonify('Added to wishlist'), 201


@bp.route('/wishlist', methods=['DELETE'])
@token_required
def delete_from_wishlist(decoded):
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

    user.wishlist.remove(product)
    db.session.delete(user)
    db.session.commit()

    return jsonify('Deleted from wishlist')