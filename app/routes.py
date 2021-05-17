from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, login
from .forms import LoginForm, EditProfileForm
from .models import User


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return redirect(url_for('your_product'))


@app.route('/your_product')
@login_required
def your_product():
    products = []
    return render_template('index.html', title='Home')


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
