from flask import request, render_template, session, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
import jsonpickle

from . import profile
# Import needed forms and models
from .forms import UserForm
from ..models import User, UserRole
# Import database object
from app import db


@profile.route('/manage')
def manage():
    users = User.query.order_by(User.role.desc()).all()
    # for user in users:
    #     print(user)
    print(len(users))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user is not None and user.verify_password(form.password.data):
    #         login_user(user, form.remember_me.data)
    #         return redirect(request.args.get('next') or url_for('auth.home'))
    #     flash('Invalid username or password.', 'error')
    return render_template('profile/manage.html', users=users, form=UserForm(role=UserRole))


@profile.route('/user_edit/<id>', methods=['GET', 'POST'])
def user_edit(id):
    user = User.query.filter_by(id=id).one()
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
    #     if user is not None and user.verify_password(form.password.data):
    #         login_user(user, form.remember_me.data)
    #         return redirect(request.args.get('next') or url_for('auth.home'))
    #     flash('Invalid username or password.', 'error')
    # return render_template('profile/manage.html', form=form)
    # return render_template('profile/manage.html', jsonify({'f': form.first_name}))
    # return jsonify({'fff': form.first_name, 'l': form.last_name})
    return jsonify({'id': user.id, 
                    'first_name': user.first_name, 
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role})