import jwt
from werkzeug.security import generate_password_hash
from flask import jsonify, request, current_app
from app.api import bp
from .errors import bad_request, not_found, unauthorized
from ..models import User
from ..middlewares import token_required


@bp.route('/auth', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()

    if not user:
        return not_found('User not found')

    if user.check_password(generate_password_hash(password)):
        return bad_request('Wrong password, please check again')

    token = jwt.encode({'id' : user.id}, current_app.config['SECRET_KEY'])

    return jsonify(token)


@bp.route('/auth/validate')
@token_required
def user_validation(decoded):
    if len(decoded.keys()) == 1 and 'id' in decoded:
        return jsonify({'id': decoded['id']})
    return unauthorized('Invalid token')
    


@bp.route('/auth/seller/validate')
@token_required
def seller_validation(decoded):
    if len(decoded.keys()) == 1 and 'seller_id' in decoded:
        return jsonify({'seller_id': decoded['seller_id']})
    return unauthorized('Invalid token')
    