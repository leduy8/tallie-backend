import requests
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from sqlalchemy import or_
from app import db
from app.products import bp
from .forms import ProductForm, SearchForm
from ..models import User, Product, Review, Picture


@bp.route('/your_product')
@login_required
def your_product():
    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(seller_id=current_user.id).paginate(
        page, current_app.config['PRODUCTS_PER_PAGE'], False
    )
    image_service_url = current_app.config['IMAGE_SERVICE_URL'] + '/images/'
    pictures = []
    for product in products.items:
        pic = Picture.query.filter_by(product_id = product.id).first()
        if pic is not None:
            pictures.append(pic.img_id)
        else:
            pictures.append(-1)

    next_url = url_for('products.your_product', page=products.next_num) if products.has_next else None
    prev_url = url_for('products.your_product', page=products.prev_num) if products.has_prev else None
    return render_template('products/products.html', title='Home', products=products, form=form, image_service_url=image_service_url, pictures=pictures, next_url=next_url, prev_url=prev_url)


@bp.route('/your_product/<id>')
@login_required
def your_product_details(id):
    product = Product.query.filter_by(id=id).first()
    reviews_users = db.session.query(Review, User).filter(Review.product_id==product.id).join(User, Review.user_id==User.id)
    pictures = Picture.query.filter_by(product_id=product.id).all()
    image_service_url = current_app.config['IMAGE_SERVICE_URL'] + '/images/'
    return render_template('products/product_details.html', product=product, reviews=reviews_users, pictures=pictures, image_service_url=image_service_url)


@bp.route('/your_product/<id>/delete')
@login_required
def your_product_delete(id):
    product = Product.query.filter_by(id=id).first()
    reviews = Review.query.filter_by(product_id=product.id).all()
    pictures = Picture.query.filter_by(product_id=product.id).all()
    db.session.delete(product)
    if reviews:
        for review in reviews:
            db.session.delete(review)
        db.session.commit()
    if pictures:
        for pic in pictures:
            url = current_app.config['IMAGE_SERVICE_URL'] + f'/images/{pic.img_id}/delete'
            req = requests.delete(
                url=url
            )
            db.session.delete(pic)
    db.session.commit()
    flash(f'Your product: {product.name} has been deleted!')
    return redirect(url_for('products.your_product'))


@bp.route('/your_product/new', methods=['GET', 'POST'])
@login_required
def your_product_new():
    form = ProductForm()

    url =  current_app.config['IMAGE_SERVICE_URL'] + '/upload_multiple'
    headers = {}
    payload = {}

    if request.method == 'POST' and form.validate_on_submit():
        if request.files['images'].filename != '':
            files = []
            for file in form.images.data:
                files.append(('pic', (file.filename, file.stream.read(), file.mimetype)))

            req = requests.post(
                url=url,
                headers=headers,
                data=payload,
                files=files
            ).json()

        product = Product(
            name=form.name.data, 
            author=form.author.data, 
            price=form.price.data, 
            quantity=form.quantity.data, 
            description=form.description.data,
            seller_id=current_user.id
        )
        db.session.add(product)
        db.session.commit()

        if request.files['images'].filename != '':
            pictures = []
            for pic in req['data']:
                pictures.append(Picture(img_id=pic['id'], product_id=product.id))
            product.pictures = pictures
        db.session.add(product)
        db.session.commit()
        flash('Your product has been added!')
        return redirect(url_for('products.your_product'))
    return render_template('products/new_product.html', form=form)


@bp.route('/your_product/<id>/edit', methods=['GET', 'POST'])
@login_required
def your_product_edit(id):
    form = ProductForm()
    product = Product.query.filter_by(id=id).first()

    upload_url =  current_app.config['IMAGE_SERVICE_URL'] + '/upload_multiple'
    headers = {}
    payload = {}

    image_service_url = current_app.config['IMAGE_SERVICE_URL'] + '/images/'
    pictures = []
    pictures_from_db = Picture.query.filter_by(product_id=product.id).all()
    for pic in pictures_from_db:
        pictures.append(pic.img_id)

    if form.validate_on_submit():
        if request.files['images'].filename != '':
            files = []
            for file in form.images.data:
                files.append(('pic', (file.filename, file.stream.read(), file.mimetype)))
                print(f'Filename = {file.filename}')
                print(f'Mimetype = {file.mimetype}')

            req = requests.post(
                url=upload_url,
                headers=headers,
                data=payload,
                files=files
            ).json()

            for pic in req['data']:
                product.pictures.append(Picture(img_id=pic['id'], product_id=product.id))

        product.name = form.name.data
        product.author = form.author.data
        product.price = form.price.data
        product.quantity = form.quantity.data
        product.description = form.description.data
        db.session.add(product)
        db.session.commit()
        flash('Your changes has been made.')
        return redirect(url_for('products.your_product', id=id))
    elif request.method == 'GET':
        form.name.data = product.name
        form.author.data = product.author
        form.price.data = product.price
        form.quantity.data = product.quantity
        form.description.data = product.description
    return render_template('products/edit_product.html', form=form, product=product, image_service_url=image_service_url, pictures=pictures)


@bp.route('/your_product/pictures/<id>/delete')
def delete_product_picture(id):
    pic = Picture.query.filter_by(img_id=id).first()
    product = Product.query.filter_by(id=pic.product_id).first()

    url = current_app.config['IMAGE_SERVICE_URL'] + f'/images/{pic.img_id}/delete'
    req = requests.delete(
        url=url
    )
    if req.status_code == 404:
        flash('Delete failed, image not found in image database.')
        return redirect(url_for('products.your_product_edit', id=product.id))
    product.pictures.remove(pic)
    db.session.add(product)
    db.session.delete(pic)
    db.session.commit()
    flash('Image deleted.')
    return redirect(url_for('products.your_product_edit', id=product.id))


@bp.route('/your_product/search', methods=['POST'])
def search_products():
    query = request.form['search']
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter(or_(Product.name.ilike(f'%{query}%'), Product.author.ilike(f'%{query}%'))).paginate(
        page, current_app.config['PRODUCTS_PER_PAGE'], False
    )
    image_service_url = current_app.config['IMAGE_SERVICE_URL'] + '/images/'
    pictures = []
    for product in products.items:
        pic = Picture.query.filter_by(product_id = product.id).first()
        if pic is not None:
            pictures.append(pic.img_id)
        else:
            pictures.append(-1)

    next_url = url_for('products.search_products', page=products.next_num) if products.has_next else None
    prev_url = url_for('products.search_products', page=products.prev_num) if products.has_prev else None
    return render_template('products/search_products.html', title='Search', products=products, image_service_url=image_service_url, pictures=pictures, next_url=next_url, prev_url=prev_url)