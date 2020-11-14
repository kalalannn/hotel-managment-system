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
    return render_template('profile/manage.html', users=users, form=UserForm())


@profile.route('/edit_user/<id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.filter_by(id=id).one()
    form = UserForm()

    if form.validate_on_submit():
        found_user = User.query.filter_by(email=form.email.data).first()
        if found_user != None and found_user.id != user.id:
            return jsonify(status=500, message='User with this email already exists!')

        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.role = form.role.data

        db.session.add(user)
        db.session.commit()
        return jsonify(status=200, message='User successfully updated.')

    return jsonify({'id': user.id, 
                    'first_name': user.first_name, 
                    'last_name': user.last_name,
                    'email': user.email,
                    'role': user.role})

@profile.route('/delete_user/<id>', methods=['GET'])
def delete_user(id):
    user = User.query.filter_by(id=id).one()

    if (user.role == UserRole.ADMIN.value):
        return jsonify(status=500, message='Cannot delete admin!')

    if (user.id == current_user.id):
        return jsonify(status=500, message='Cannot delete current user!')

    # Hotel.query.filter_by(owner=user).all()
    db.session.delete(user)
    db.session.commit()
    return jsonify(status=200, message='User successfully deleted.')