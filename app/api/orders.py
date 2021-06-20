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

#     # TODO Xử lý order api: Gửi order từ server đến 2 service shipping với payment,
#     # TODO gửi đến shipping để bên shipping nhận order, gửi đến payment để thanh toán.

#     # TODO Xử lý trường hợp request post fail ở 1 hay cả 2 service vệ tinh

#     # TODO Xử lý order view: Lấy tất cả order, lấy order details.

#     token = user.get_generate_token()
#     shipping_url = current_app.config['SHIPPING_SERVICE_URL'] + '/api/orders'
#     data_shipping = {
#         'productId': data['product_id'],
#         'quantity': data['quantity'],
#         'recipientName': data['recipient_name'],
#         'recipientPhone': data['recipient_phone'],
#         'deliverTo': data['deliver_to']
#     }

#     req_shipping = requests.post(
#         url=shipping_url,
#         data=data_shipping,
#         headers={
#             'Content-Type': 'application/json',
#             'X-Auth-Token': token
#         }
#     )

#     payment_url = current_app.config['PAYMENT_SERVICE_URL'] + '/api/cards/'
#     data_payment = {
#         # ! Recheck data for executing transfer procedure
#     }

#     req_payment = requests.post(
#         url=payment_url,
#         data=data_payment,
#         headers={
#             'Content-Type': 'application/json',
#             # ? What in here specifically
#             # 'X-Credentials': token
#         }
#     )

#     return 'OK'