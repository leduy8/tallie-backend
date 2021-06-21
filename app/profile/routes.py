from datetime import datetime
import requests
from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import current_user, login_required
from app import db
from app.profile import bp
from .forms import ProfileForm, PaymentForm
from ..models import Payment, Avatar, User


@bp.route('/profile')
@login_required
def profile():
    payment = Payment.query.filter_by(user_id=current_user.id).first()
    return render_template('profile/profile.html', title='Profile', user=current_user, payment=payment)


@bp.route('/profile/info/edit', methods=['GET', 'POST'])
@login_required
def edit_profile_info():
    form = ProfileForm()

    payment = Payment.query.filter_by(user_id=current_user.id).first()

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email has already in use by another account.')
            return redirect(url_for('profile.profile'))
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        current_user.bio = form.bio.data
        if current_user.email != form.email.data:
            current_user.email_activated = False
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes has been made.')
        return redirect(url_for('profile.profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.phone.data = current_user.phone
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.bio.data = current_user.bio
    return render_template('profile/edit_profile.html', title='Edit Profile', form=form, user=current_user, payment=payment)


@bp.route('/profile/payment/edit')
def edit_profile_payment():
    form = PaymentForm()

    payment_data_from_db = Payment.query.filter_by(user_id=current_user.id).first()
    url = current_app.config['PAYMENT_SERVICE_URL'] + '/api/cards/info'
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
    return render_template('profile/edit_payment.html', title='Edit Payment', form=form, user=current_user, payment=payment)


@bp.route('/profile/payment/delete')
def delete_profile_payment():
    payment = Payment.query.filter_by(user_id=current_user.id).first()
    db.session.delete(payment)
    db.session.commit()
    flash('Your payment has been deleted.')
    return redirect(url_for('profile.profile'))


@bp.route('/profile/payment/new', methods=['GET', 'POST'])
def new_profile_payment():
    form = PaymentForm()
    url = current_app.config['PAYMENT_SERVICE_URL'] + '/api/cards/validate'
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

        return redirect(url_for('profile.profile'))
    return render_template('profile/new_payment.html', title='New Payment', form=form, user=current_user, payment=None)
