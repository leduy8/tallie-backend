import json
import requests
from flask import jsonify, request, current_app
from app import db
from app.api import bp
from .errors import bad_request, not_found, internal_server_error
from ..models import User, Payment, Product
from ..middlewares import token_required


@bp.route('/orders', methods=['POST'])
@token_required
def create_order(decoded):
    user = User.query.filter_by(id=decoded['id']).first()
    data = request.get_json()
    product = Product.query.filter_by(id=data['product_id']).first()

    if not user:
        return not_found('User\'s not found')

    if not product:
        return bad_request('Product\'s not found')

    if product.quantity < data['quantity']:
        return bad_request('Order cannot be processed due to products in stock is not enough for the order.')

    buyer_payment = Payment.query.filter_by(user_id=user.id).first()
    seller_payment = Payment.query.filter_by(user_id=product.seller_id).first()

    if not buyer_payment:
        return bad_request('Buyer hasn\'t register a banking card.')

    if not seller_payment:
        return bad_request('Seller hasn\'t register a banking card.')

    if 'product_id' not in data or 'quantity' not in data or 'card_number' not in data or 'recipient_name' not in data or 'recipient_phone' not in data or 'deliver_to' not in data:
        return bad_request('Please input all fields for order\'s creation.')

    if type(data['product_id']) is not int or type(data['quantity']) is not int or type(data['card_number']) is not str or type(data['recipient_name']) is not str or type(data['recipient_phone']) is not str or type(data['deliver_to']) is not str:
        return bad_request('Please recheck all field inputs data types.')

    token = user.get_validate_token()
    shipping_post_order_url = current_app.config['SHIPPING_SERVICE_URL'] + '/api/orders'
    data_shipping = {
        'productId': data['product_id'],
        'quantity': data['quantity'],
        'recipientName': data['recipient_name'],
        'recipientPhone': data['recipient_phone'],
        'deliverTo': data['deliver_to']
    }

    req_shipping = requests.post(
        url=shipping_post_order_url,
        json=data_shipping,
        headers={
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        }
    )

    if req_shipping.status_code == 400:
        return internal_server_error('Something went wrong with the server. Please try again in another time. 123')

    payment_url = current_app.config['PAYMENT_SERVICE_URL'] + '/api/cards/transfer'
    data_payment = {
        'to': seller_payment.card_number,
        'amount': product.price * data['quantity']
    }

    req_payment = requests.post(
        url=payment_url,
        json=data_payment,
        headers={
            'Content-Type': 'application/json',
            'X-Credentials': buyer_payment.credentials
        }
    )

    if req_payment.status_code == 400 or req_payment.status_code == 401:
        shipping_delete_order_url = current_app.config['SHIPPING_SERVICE_URL'] + '/api/orders/' + req_shipping.json()['id']
        req_shipping_delete = requests.delete(
            url=shipping_delete_order_url,
            headers={
                'Content-Type': 'application/json',
                'X-Auth-Token': token
            }
        )

        if req_shipping_delete.status_code == 400:
            return internal_server_error('Something went wrong with the server. Please try again in another time. 456')

        return internal_server_error('Something went wrong with the server. Please try again in another time. 789')

    product.quantity = product.quantity - data['quantity']
    db.session.add(product)
    db.session.commit()

    return jsonify(req_shipping.json()), 201