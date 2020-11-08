from flask import request, render_template, session, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from . import auth
# Import needed forms and models
from .forms import LoginForm
from ..models import User
# Import database object
from app import db

# Set the route and accepted methods
# Important! call it like url_for('auth.login')
@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('auth.home'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@auth.route('/home/', methods=['GET'])
def home():
    return render_template('auth/home.html')