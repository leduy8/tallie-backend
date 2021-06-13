import requests
from flask import jsonify, request, current_app
from app import db
from app.api import bp
from .errors import bad_request, not_found
from ..models import Payment, User
from ..middlewares import token_required


@bp.route('/payments', methods=['GET'])
@token_required
def get_payment_info(decoded):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    payment = Payment.query.filter_by(user_id=user.id).first()

    if not payment:
        return not_found('User haven\'t connect to any card.')

    return jsonify(payment.get_payment_info())


@bp.route('/payments', methods=['POST'])
@token_required
def payment_register(decoded):
    user = User.query.filter_by(id=decoded['id']).first()
    data = request.get_json()

    if not user:
        return not_found('User\'s not found')

    if 'card_number' not in data or 'name' not in data or 'start_date' not in data or 'end_date' not in data:
        return bad_request('Please input all fields.')

    url = current_app.config['PAYMENT_SERVICE_URL'] + '/api/cards/validate'

    req = requests.post(
        url=url,
        json=data
    )

    if req.status_code == 400 or req.status_code == 401:
        return bad_request('Connect failed, invalid infomations.')

    payment = Payment(card_number=data['card_number'], credentials=req.text, user_id=user.id)
    try:
        db.session.add(payment)
        db.session.commit()
    except Exception as e:
        print(e)
    return jsonify('Connected to your card'), 201


@bp.route('/payments', methods=['DELETE'])
@token_required
def payment_deregister(decoded):
    user = User.query.filter_by(id=decoded['id']).first()

    if not user:
        return not_found('User\'s not found')

    payment = Payment.query.filter_by(user_id=user.id).first()

    db.session.delete(payment)
    db.session.commit()

    return jsonify('Deconnected to your card')