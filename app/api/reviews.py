from flask import jsonify, request, current_app
from app import db
from app.api import bp
from .errors import bad_request, not_found
from ..models import Product, User, Review, Abuse, Helpful
from ..middlewares import token_required


@bp.route('/products/<product_id>/reviews', methods=['GET'])
def get_all_reviews(product_id):
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.filter_by(product_id=product_id).paginate(
        page, current_app.config['REVIEWS_PER_PAGE'], False
    )
    next_page = page=reviews.next_num if reviews.has_next else None
    prev_page = page=reviews.prev_num if reviews.has_prev else None

    return jsonify({
        'reviews': [review.get_review_info() for review in reviews.items],
        '_meta': {
            'page': page or 1,
            'per_page': current_app.config['REVIEWS_PER_PAGE'],
            'total_pages': reviews.pages,
            'total_items': reviews.total,
            'next_page': next_page,
            'prev_page': prev_page
        }
    })


@bp.route('/products/<product_id>/reviews', methods=['POST'])
@token_required
def post_a_review(decoded, product_id):
    user = User.query.filter_by(id=decoded['id']).first()
    data = request.get_json()

    if not user:
        return not_found('User\'s not found')

    if Review.query.filter_by(user_id=user.id).filter_by(product_id=product_id).first():
        return bad_request('User can only have 1 review per product.')

    if 'star' not in data or 'overview' not in data or 'content' not in data or 'prevent_spoiler' not in data:
        return bad_request('Not enough infomation for posting a review.')

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return not_found('Product\'s not found')

    review = Review(
        user_id = user.id,
        product_id = product.id,
        star = data['star'],
        overview = data['overview'],
        content = data['content'],
        prevent_spoiler = data['prevent_spoiler']
    )

    if 'started_reading' in data:
        review.started_reading = data['started_reading']
        if 'finished_reading' in data:
            review.finished_reading = data['finished_reading']

    db.session.add(review)
    db.session.commit()

    return jsonify(review.get_review_info()), 201


@bp.route('/products/<product_id>/reviews', methods=['PUT'])
@token_required
def edit_a_review(decoded, product_id):
    user = User.query.filter_by(id=decoded['id']).first()
    data = request.get_json()

    if not user:
        return not_found('User\'s not found')

    if 'star' not in data or 'overview' not in data or 'content' not in data or 'prevent_spoiler' not in data:
        return bad_request('Not enough infomation for posting a review.')

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return not_found('Product\'s not found')

    review = Review.query.filter_by(user_id=user.id).filter_by(product_id=product_id).first()

    review.star = data['star'],
    review.overview = data['overview'],
    review.content = data['content'],
    review.prevent_spoiler = data['prevent_spoiler']

    if 'started_reading' in data:
        review.started_reading = data['started_reading']
        if 'finished_reading' in data:
            review.finished_reading = data['finished_reading']

    db.session.add(review)
    db.session.commit()

    return jsonify(review.get_review_info())


@bp.route('/products/<product_id>/reviews', methods=['DELETE'])
@token_required
def delete_a_review(decoded, product_id):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return not_found('Product\'s not found')

    review = Review.query.filter_by(user_id=user.id).filter_by(product_id=product_id).first()

    db.session.delete(review)
    db.session.commit()

    return jsonify('Review deleted')


@bp.route('/products/<product_id>/reviews/<review_id>/abuse', methods=['POST'])
@token_required
def report_abuse(decoded, product_id, review_id):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return not_found('Product\'s not found')

    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return not_found('Review\'s not found')

    if Abuse.query.filter_by(user_id=user.id).filter_by(review_id=review.id).first():
        return bad_request('User can only send one abuse report per product.')

    if Helpful.query.filter_by(user_id=user.id).filter_by(review_id=review.id).first():
        helpful = Helpful.query.filter_by(user_id=user.id).filter_by(review_id=review.id).first()
        review.helpfuls.remove(helpful)
        db.session.delete(helpful)
        db.session.commit()

    abuse = Abuse(review_id=review.id, user_id=user.id)

    review.abuses.append(abuse)
    db.session.add(review)
    db.session.add(abuse)
    db.session.commit()

    return jsonify('Abuse report has been sent'), 201


@bp.route('/products/<product_id>/reviews/<review_id>/abuse', methods=['DELETE'])
@token_required
def delete_abuse_report(decoded, product_id, review_id):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return not_found('Product\'s not found')

    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return not_found('Review\'s not found')

    abuse = Abuse.query.filter_by(user_id=user.id).filter_by(review_id=review.id).first()

    if not abuse:
        return not_found('User\'s abuse report not found')

    review.abuses.remove(abuse)
    db.session.delete(abuse)
    db.session.commit()

    return jsonify('Abuse report has been deleted.')


@bp.route('/products/<product_id>/reviews/<review_id>/helpful', methods=['POST'])
@token_required
def find_helpful(decoded, product_id, review_id):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return not_found('Product\'s not found')

    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return not_found('Review\'s not found')

    if Helpful.query.filter_by(user_id=user.id).filter_by(review_id=review.id).first():
        return bad_request('User can only send one find helpful report per product.')

    if Abuse.query.filter_by(user_id=user.id).filter_by(review_id=review.id).first():
        abuse = Abuse.query.filter_by(user_id=user.id).filter_by(review_id=review.id).first()
        review.abuses.remove(abuse)
        db.session.delete(abuse)
        db.session.commit()

    helpful = Helpful(review_id=review.id, user_id=user.id)

    review.helpfuls.append(helpful)
    db.session.add(review)
    db.session.add(helpful)
    db.session.commit()

    return jsonify('Find helpful report has been sent'), 201


@bp.route('/products/<product_id>/reviews/<review_id>/helpful', methods=['DELETE'])
@token_required
def delete_find_helpful(decoded, product_id, review_id):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    product = Product.query.filter_by(id=product_id).first()

    if not product:
        return not_found('Product\'s not found')

    review = Review.query.filter_by(id=review_id).first()

    if not review:
        return not_found('Review\'s not found')

    helpful = Helpful.query.filter_by(user_id=user.id).filter_by(review_id=review.id).first()

    if not helpful:
        return not_found('User\'s find helpful report not found')

    review.helpfuls.remove(helpful)
    db.session.delete(helpful)
    db.session.commit()

    return jsonify('Find helpful report has been deleted.')