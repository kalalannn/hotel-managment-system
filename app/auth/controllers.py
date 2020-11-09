from flask import request, render_template, session, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from . import auth
# Import needed forms and models
from .forms import LoginForm, RegistrationForm, NewPasswordForm
from ..models import User
# Import database object
from app import db
from app.helpers import Helper

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
        flash('Invalid username or password.', 'error')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if User.has_role(current_user, 'ADMIN'):
        choises = Helper.dictToListOfTuples(User._roles, True)
        # choises.insert(0, ('','')) # If you want to add an empty option
        form.role.choices = choises
    else:
        del form.role

    # POST
    if form.validate_on_submit():
        user = User(form.first_name.data,
                    form.last_name.data,
                    form.email.data,
                    form.password.data,
                    (form.role.data if User.has_role(current_user, 'ADMIN') else 'CUSTOMER'))
        db.session.add(user)
        db.session.commit()
        flash('You can now log in.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/new_password', methods=['GET', 'POST'])
@login_required
def new_password():
    form = NewPasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.password = form.new_password.data
            db.session.commit()
            logout_user()
            flash('You can now log in with a new password.', 'info')
            return redirect(url_for('auth.login'))
        flash('You entered wrong current password.', 'error')
    return render_template('auth/new_password.html', form=form)


@auth.route('/home/', methods=['GET'])
def home():
    return render_template('auth/home.html')
