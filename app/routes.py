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


@app.route('/your_product/new')
@login_required
def your_product_new():
    form = ProductForm()
    return render_template('new_product.html', form=form)


@app.route('/your_product/<id>/edit')
@login_required
def your_product_edit(id):
    form = ProductForm()
    product = {
        'id': 6,
        'name': 'Product 6',
        'price': 150000,
        'quantity': 13,
        'description': 'Product 6 description',
        'pictures': [
            'https://worldwideinterweb.com/wp-content/uploads/2017/10/book20title20fail.png',
            'http://pm1.narvii.com/6727/a84c910fa744274dc0ad7ebb14d9cd8a8a3401dfv2_00.jpg',
            'https://i.pinimg.com/originals/d3/fa/4a/d3fa4a70c6571e238490b2c3cc179186.jpg'
        ]
    }
    return render_template('edit_product.html', form=form, product=product)


@app.route('/profile')
@login_required
def profile():
    user = {
        'username': 'duy123',
        'phone': '0987654321',
        'email': 'duy@duy.com',
        'bio': 'This is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long text lol',
        'address': '121 Thái Hà, Thanh Xuân, Hà Nội',
    }
    return render_template('profile.html', title='Profile', user=user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = {
        'username': 'duy123',
        'phone': '0987654321',
        'email': 'duy@duy.com',
        'bio': 'This is a very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very very long text lol',
        'address': '121 Thái Hà, Thanh Xuân, Hà Nội',
    }
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
    return render_template('edit_profile.html', title='Edit Profile', form=form, user=user)


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
