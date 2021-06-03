from datetime import datetime
import requests
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, login
from .forms import LoginForm, EditProfileForm, ProductForm
from .models import User, Product, Review


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
    next_url = url_for('your_product', page=products.next_num) if products.has_next else None
    prev_url = url_for('your_product', page=products.prev_num) if products.has_prev else None
    return render_template('products.html', title='Home', products=products, next_url=next_url, prev_url=prev_url)


@app.route('/your_product/<id>')
@login_required
def your_product_details(id):
    product = Product.query.filter_by(id=id).first()
    reviews_users = db.session.query(Review, User).filter(Review.product_id==product.id).join(User, Review.user_id==User.id)
    return render_template('product_details.html', product=product, reviews=reviews_users)


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
    if form.validate_on_submit():
        # print(form.image.data)
        # req = requests.post('http://192.169.1.67:5000/images', data={'image': form.image.data})
        # print(req)

        product = Product(
            name=form.name.data, 
            author=form.author.data, 
            price=form.price.data, 
            quantity=form.quantity.data, 
            description=form.description.data,
            seller_id=current_user.id
        )
        print(product)
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
    if form.validate_on_submit():
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
    return render_template('edit_product.html', form=form, product=product)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile', user=current_user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
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
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=current_user)


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