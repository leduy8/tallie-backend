from datetime import date, datetime
import requests
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, login
from .forms import LoginForm, ProfileForm, ProductForm, PaymentForm
from .models import Payment, User, Product, Review, Picture, Avatar
from .email import send_verify_email_email


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return redirect(url_for('your_product'))


@app.route('/your_product')
@login_required
def your_product():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(seller_id=current_user.id).paginate(
        page, app.config['PRODUCTS_PER_PAGE'], False
    )
    image_service_url = app.config['IMAGE_SERVICE_URL'] + '/images/'
    pictures = []
    for product in products.items:
        pic = Picture.query.filter_by(product_id = product.id).first()
        pictures.append(pic.img_id)

    next_url = url_for('your_product', page=products.next_num) if products.has_next else None
    prev_url = url_for('your_product', page=products.prev_num) if products.has_prev else None
    return render_template('products.html', title='Home', products=products, image_service_url=image_service_url, pictures=pictures, next_url=next_url, prev_url=prev_url)


@app.route('/your_product/<id>')
@login_required
def your_product_details(id):
    product = Product.query.filter_by(id=id).first()
    reviews_users = db.session.query(Review, User).filter(Review.product_id==product.id).join(User, Review.user_id==User.id)
    pictures = Picture.query.filter_by(product_id=product.id).all()
    image_service_url = app.config['IMAGE_SERVICE_URL'] + '/images/'
    return render_template('product_details.html', product=product, reviews=reviews_users, pictures=pictures, image_service_url=image_service_url)


@app.route('/your_product/<id>/delete')
@login_required
def your_product_delete(id):
    product = Product.query.filter_by(id=id).first()
    reviews = Review.query.filter_by(product_id=product.id).all()
    db.session.delete(product)
    for review in reviews:
        db.session.delete(review)
    db.session.commit()
    flash(f'Your product: {product.name} has been deleted!')
    return redirect(url_for('your_product'))


@app.route('/your_product/new', methods=['GET', 'POST'])
@login_required
def your_product_new():
    form = ProductForm()

    url =  app.config['IMAGE_SERVICE_URL'] + '/upload_multiple'
    headers = {}
    payload = {}

    if request.method == 'POST' and form.validate_on_submit():
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

        pictures = []
        for pic in req['data']:
            pictures.append(Picture(img_id=pic['id'], product_id=product.id))
        product.pictures = pictures
        db.session.add(product)
        db.session.commit()
        flash('Your product has been added!')
        return redirect(url_for('your_product'))
    return render_template('new_product.html', form=form)


@app.route('/your_product/<id>/edit', methods=['GET', 'POST'])
@login_required
def your_product_edit(id):
    form = ProductForm()
    product = Product.query.filter_by(id=id).first()

    upload_url =  app.config['IMAGE_SERVICE_URL'] + '/upload_multiple'
    headers = {}
    payload = {}

    image_service_url = app.config['IMAGE_SERVICE_URL'] + '/images/'
    pictures = []
    pictures_from_db = Picture.query.filter_by(product_id=product.id).all()
    for pic in pictures_from_db:
        pictures.append(pic.img_id)

    if form.validate_on_submit():
        files = []
        for file in form.images.data:
            files.append(('pic', (file.filename, file.stream.read(), file.mimetype)))

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
        return redirect(url_for('your_product', id=id))
    elif request.method == 'GET':
        form.name.data = product.name
        form.author.data = product.author
        form.price.data = product.price
        form.quantity.data = product.quantity
        form.description.data = product.description
    return render_template('edit_product.html', form=form, product=product, image_service_url=image_service_url, pictures=pictures)


@app.route('/your_product/pictures/<id>/delete')
def delete_product_picture(id):
    pic = Picture.query.filter_by(img_id=id).first()
    product = Product.query.filter_by(id=pic.product_id).first()

    url = app.config['IMAGE_SERVICE_URL'] + f'/images/{pic.img_id}/delete'
    req = requests.delete(
        url=url
    )
    if req.status_code == 404:
        flash('Delete failed, image not found in image database.')
        return redirect(url_for('your_product_edit', id=product.id))
    product.pictures.remove(pic)
    db.session.add(product)
    db.session.delete(pic)
    db.session.commit()
    flash('Image deleted.')
    return redirect(url_for('your_product_edit', id=product.id))


@app.route('/profile')
@login_required
def profile():
    payment = Payment.query.filter_by(user_id=current_user.id).first()
    return render_template('profile.html', title='Profile', user=current_user, payment=payment)


@app.route('/profile/info/edit', methods=['GET', 'POST'])
@login_required
def edit_profile_info():
    form = ProfileForm()

    payment = {
        'card_number': '123456789012345',
        'credentials': 'asdasd1as231d32a1asdasd15',
        'user_id': '1'
    }

    if form.validate_on_submit():
        # current_user.username = form.username.data
        current_user.phone = form.phone.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your changes has been made.')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.phone.data = current_user.phone
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.bio.data = current_user.bio
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=current_user, payment=payment)


@app.route('/profile/payment/edit')
def edit_profile_payment():
    form = PaymentForm()

    payment_data_from_db = Payment.query.filter_by(user_id=current_user.id).first()
    url = app.config['PAYMENT_SERVICE_URL'] + '/api/cards/info'
    headers = {'X-Credentials': str(payment_data_from_db.credentials)}

    payment = requests.get(
        url=url,
        headers=headers
    ).json()
    
    if request.method == 'GET':
        form.card_number.data = payment['card_number']
        form.card_owner_name.data = payment['name']
        form.start_date.data = datetime.strptime(payment['start_date'], '%Y-%m-%d')
        form.end_date.data = datetime.strptime(payment['end_date'], '%Y-%m-%d')
        form.cvc.data = payment['cvc']
    return render_template('edit_payment.html', title='Edit Payment', form=form, user=current_user, payment=payment)


@app.route('/profile/payment/delete')
def delete_profile_payment():
    payment = Payment.query.filter_by(user_id=current_user.id).first()
    db.session.delete(payment)
    db.session.commit()
    flash('Your payment has been deleted.')
    return redirect(url_for('profile'))


@app.route('/profile/payment/new', methods=['GET', 'POST'])
def new_profile_payment():
    form = PaymentForm()
    url = app.config['PAYMENT_SERVICE_URL'] + '/api/cards/validate'

    if form.validate_on_submit():
        req = requests.post(
            url=url,
            json={
                'card_number': form.card_number.data,
                'name': form.card_owner_name.data,
                'start_date': form.start_date.data.strftime('%Y-%m-%d'),
                'end_date': form.end_date.data.strftime('%Y-%m-%d'),
                'cvc': form.cvc.data
            }
        )
        if (req.status_code == 200):
            new_payment = Payment(card_number=form.card_number.data, credentials=req.text, user_id=current_user.id)
            db.session.add(new_payment)
            db.session.commit()
            flash('Your new payment has been created.')
        elif (req.status_code == 400 or req.status_code == 401):
            flash('You have input wrong infomation, please check again.')
        elif (req.status_code == 404):
            return render_template('404.html')

        return redirect(url_for('profile'))
    return render_template('edit_payment.html', title='New Payment', form=form, user=current_user, payment=None)


@app.route('/orders')
def orders():
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
    return render_template('orders.html', orders=orders)


@app.route('/orders/<id>')
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
    return render_template('orders_details.html', order=order, product=product)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('your_product'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('your_product'))
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/verify_email_request')
@login_required
def verify_email_request():
    send_verify_email_email(current_user)
    flash('An email verification has been sent, please check your mail.')
    return redirect(url_for('profile'))


@app.route('/verify_email/<token>', methods=['GET', 'POST'])
@login_required
def verify_email(token):
    user = User.verify_generated_token(token)
    if not user:
        return redirect(url_for('index'))
    user.email_activated = True
    db.session.add(user)
    db.session.commit()
    return render_template('email/verify_email_success.html')
    # flash('Your email has been verified!')
    # return redirect(url_for('profile'))