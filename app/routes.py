from flask import render_template, flash, redirect, url_for
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/your_product')
def your_product():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login as user {form.username.data}')
        return redirect(url_for('your_product'))
    return render_template('login.html', title='Login', form=form)