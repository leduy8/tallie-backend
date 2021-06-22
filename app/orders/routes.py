from app.models import Product
import requests
from flask import render_template, current_app, url_for
from flask_login import current_user
from app.orders import bp


@bp.route('/orders')
def orders():
    token = current_user.get_seller_token()
    url = current_app.config['SHIPPING_SERVICE_URL'] + '/api/orders'
    req = requests.get(
        url=url,
        headers={
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        }
    )

    data = req.json()

    orders = data['orders']
    prev_url = url_for('orders.orders', page=data['_meta']['prevPage']) if data['_meta']['prevPage'] else None
    next_url = url_for('orders.orders', page=data['_meta']['nextPage']) if data['_meta']['nextPage'] else None

    return render_template('orders/orders.html', orders=orders, prev_url=prev_url, next_url=next_url)


@bp.route('/orders/<id>')
def orders_details(id):
    token = current_user.get_seller_token()
    url = current_app.config['SHIPPING_SERVICE_URL'] + '/api/orders/' + id
    image_service_url = current_app.config['IMAGE_SERVICE_URL'] + '/images/'
    req = requests.get(
        url=url,
        headers={
            'Content-Type': 'application/json',
            'X-Auth-Token': token
        }
    )

    order = req.json()
    product = Product.query.filter_by(id=order['productId']).first()

    return render_template('orders/orders_details.html', order=order, image_service_url=image_service_url, product=product.get_product_info())