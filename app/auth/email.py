from flask import render_template, current_app
from app.email import send_email


def send_verify_email_email(user):
    token = user.get_generate_token()
    send_email(
        subject='[Tallie] Verify your email',
        sender=current_app.config['ADMINS'][0],
        recipients=[user.email],
        text_body=render_template('email/verify_email.txt', user=user, token=token),
        html_body=render_template('email/verify_email.html', user=user, token=token)
    )