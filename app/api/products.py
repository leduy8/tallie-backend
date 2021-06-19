from flask import jsonify, request, current_app
from sqlalchemy import or_, and_, func
from app import db
from app.api import bp
from .errors import bad_request, not_found
from ..models import Product, Review, Seen


def get_price_range(price_range):
    min = ''
    max = ''
    flag = False
    for char in price_range:
        if char == ',':
            flag = True
            continue
        if flag == False:
            min += char
        if flag == True:
            max += char

    return float(min), float(max)


@bp.route('/products/featured')
def featured_products():
    # ? Sort by review's stars of each product
    page = request.args.get('page', 1, type=int)
    featured = db.session.query(Product, func.sum(Review.star)).join(Product).filter(
        Review.product_id==Product.id).group_by(Product.id).order_by(func.sum(Review.star).desc()).paginate(
            page, current_app.config['PRODUCTS_PER_PAGE'], False
        )
    next_page = page=featured.next_num if featured.has_next else None
    prev_page = page=featured.prev_num if featured.has_prev else None

    return jsonify({
        'data': [product_count[0].get_product_info() for product_count in featured.items],
        '_meta': {
            'page': page or 1,
            'per_page': current_app.config['PRODUCTS_PER_PAGE'],
            'total_pages': featured.pages,
            'total_items': featured.total,
            'next_page': next_page,
            'prev_page': prev_page
        }
    })


@bp.route('/products/best_selling_this_month')
def best_selling_products():
    pass


@bp.route('/products/most_viewed')
def most_viewed_products():
    # ? db.session.execute('SELECT product, count(seen.product_id) FROM product LEFT JOIN seen ON product.id = seen.product_id GROUP BY product ORDER BY count(seen.product_id) DESC')

    page = request.args.get('page', 1, type=int)
    products_counts = db.session.query(Product, func.count(Seen.product_id)).join(Product).filter(
        Seen.product_id == Product.id).group_by(Product.id).order_by(func.count(Seen.product_id).desc()).paginate(
            page, current_app.config['PRODUCTS_PER_PAGE'], False
        )
    next_page = page=products_counts.next_num if products_counts.has_next else None
    prev_page = page=products_counts.prev_num if products_counts.has_prev else None

    return jsonify({
        'data': [{'product': product_count[0].get_product_info(), 'count': product_count[1]} for product_count in products_counts.items],
        '_meta': {
            'page': page or 1,
            'per_page': current_app.config['PRODUCTS_PER_PAGE'],
            'total_pages': products_counts.pages,
            'total_items': products_counts.total,
            'next_page': next_page,
            'prev_page': prev_page
        }
    })



@bp.route('/products/search')
def searched_products():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('name', type=str)
    price_range = request.args.get('price_range', type=tuple)
    author = request.args.get('author', type=str)

    if not query:
        return bad_request('Search query must have value.')

    products = None
    
    min_price, max_price = get_price_range(price_range)

    if price_range and author:
        products = Product.query.filter(or_(Product.name.ilike(f'%{query}%'), Product.author.ilike(f'%{author}%'))).filter(and_(Product.price > min_price, Product.price < max_price)).paginate(
            page, current_app.config['PRODUCTS_PER_PAGE'], False
        )
    elif price_range:
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).filter(and_(Product.price > min_price, Product.price < max_price)).paginate(
            page, current_app.config['PRODUCTS_PER_PAGE'], False
        )
    elif author:
        products = Product.query.filter(or_(Product.name.ilike(f'%{query}%'), Product.author.ilike(f'%{author}%'))).paginate(
            page, current_app.config['PRODUCTS_PER_PAGE'], False
        )
    else:
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).paginate(
            page, current_app.config['PRODUCTS_PER_PAGE'], False
        )

    next_page = products.next_num if products.has_next else None
    prev_page = products.prev_num if products.has_prev else None

    return jsonify({
        'products': [product.get_product_info() for product in products.items],
        '_meta': {
            'page': page or 1,
            'per_page': current_app.config['PRODUCTS_PER_PAGE'],
            'total_pages': products.pages,
            'total_items': products.total,
            'next_page': next_page,
            'prev_page': prev_page
        }
    })


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