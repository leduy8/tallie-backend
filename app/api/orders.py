from flask.globals import current_app
import requests
from flask import jsonify, request
from app.api import bp
from .errors import bad_request, not_found
from ..models import User
from ..middlewares import token_required


# @bp.route('/orders', methods=['POST'])
# @token_required
# def create_order(decoded):
#     user = User.query.filter_by(id=decoded['id']).first()
#     data = request.get_json()

#     if not user:
#         return not_found('User\'s not found')

#     if 'product_id' not in data or 'quantity' not in data or 'card_number' not in data or 'recipient_name' not in data or 'recipient_phone' not in data or 'deliver_to' not in data:
#         return bad_request('Please input all fields for order\'s creation.')

#     if type(data['product_id']) is not int or type(data['quantity']) is not int or type(data['card_number']) is not str or type(data['recipient_name']) is not str or type(data['recipient_phone']) is not str or type(data['deliver_to']) is not str:
#         return bad_request('Please recheck all field inputs data types.')

#     # !!! Not done, wait for shipping service to deploy
#     # !!! Not done, wait for shipping service to deploy
#     # !!! Not done, wait for shipping service to deploy

#     url = current_app.config['SHIPPING_SERVICE_URL'] + 'whatever-it-is'
#     data = {}

#     req = requests.post(
#         url=url,
#         data=data
#     )

#     return 'OK'