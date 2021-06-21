from datetime import datetime
import requests
from flask import render_template, current_app, request, url_for
from flask_login import current_user
from app.orders import bp


@bp.route('/orders')
def orders():
    # token = current_user.get_validate_token()
    # url = current_app.config['SHIPPING_SERVICE_URL'] + '/api/orders'
    # req = requests.get(
    #     url=url,
    #     headers={
    #         'Content-Type': 'application/json',
    #         'X-Auth-Token': token
    #     }
    # )

    # data = req.json()

    # page = request.args.get('page', 1, type=int)
    # orders = data['orders']
    # next_url = url_for('products.search_products', page=data['_meta']['nextPage']) if data['_meta']['nextPage'] else None
    # prev_url = url_for('products.search_products', page=data['_meta']['prevPage']) if data['_meta']['prevPage'] else None

    # print(page)
    # print(orders)
    # print(next_url)
    # print(prev_url)

    orders = [
        {
            'id': 1,
            'user_id': 1,
            'product_id': 1,
            'created_at': datetime(2021, 3, 5, 16, 30, 00)
        },
        {
            'id': 2,
            'user_id': 2,
            'product_id': 1,
            'created_at': datetime(2021, 3, 1, 16, 30, 00)
        },
        {
            'id': 3,
            'user_id': 3,
            'product_id': 1,
            'created_at': datetime(2021, 3, 5, 6, 30, 00)
        },
        {
            'id': 4,
            'user_id': 2,
            'product_id': 1,
            'created_at': datetime(2021, 3, 5, 22, 00, 00)
        }
    ]
    # return render_template('orders/orders.html', orders=orders, prev_url=prev_url, next_url=next_url)
    return render_template('orders/orders.html', orders=orders)


@bp.route('/orders/<id>')
def orders_details(id):
    order = {
        'id': 1,
        'userId': 1,
        'productId': 1,
        'createdAt': datetime(2021, 3, 5, 16, 30, 00),
        'recipientName': 'Duy Le',
        'recipientPhone': '0987654321',
        'deliverTo': '121 Thai Ha, Thanh Xuan, Ha Noi',
        'estimatingDateArrival': datetime(2020, 10, 3),
        'hasTaken': True,
        'isDelivering': False,
        'isDelivered': False
    }
    product = {
        'product_id': 1,
        'name': 'Little Bobby',
        'pictures': [
            'https://worldwideinterweb.com/wp-content/uploads/2017/10/book20title20fail.png',
            'http://pm1.narvii.com/6727/a84c910fa744274dc0ad7ebb14d9cd8a8a3401dfv2_00.jpg',
            'https://i.pinimg.com/originals/d3/fa/4a/d3fa4a70c6571e238490b2c3cc179186.jpg'
        ],
        'price': 40000,
        'quantity': 1
    }
    return render_template('orders/orders_details.html', order=order, product=product)