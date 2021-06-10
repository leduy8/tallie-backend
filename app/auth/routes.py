from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db, login
from app.auth import bp
from .forms import LoginForm
from .email import send_verify_email_email
from ..models import User

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('your_product'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('auth.login')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('your_product'))
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/verify_email_request')
@login_required
def verify_email_request():
    send_verify_email_email(current_user)
    flash('An email verification has been sent, please check your mail.')
    return redirect(url_for('profile'))


@bp.route('/verify_email/<token>', methods=['GET', 'POST'])
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