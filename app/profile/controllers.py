from flask import request, render_template, session, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
import jsonpickle

from . import profile
# Import needed forms and models
from .forms import UserForm, UserSearchForm
from ..models import User, UserRole, Hotel
# Import database object
from app import db


@profile.route('/manage', methods=['GET', 'POST'])
def manage():
    user_search_form = UserSearchForm(role=0)
    # find all users for admin, subordinates for director
    users = User.query.filter_by(is_active=True).order_by(User.role.desc()).all()
    if current_user.role == UserRole.DIRECTOR.value:
        users = list(filter(lambda u: u.role < UserRole.DIRECTOR.value, users))

    if (session.get('formdata')):
        formdata = session.get('formdata')
        user_search_form = UserSearchForm(
            first_name=formdata['first_name'], \
            last_name=formdata['last_name'], \
            email=formdata['email'], \
            role=int(formdata['role']))
        session.pop('formdata')

    if (session.get('usersdata')):
        usersdata = session.get('usersdata')
        users = jsonpickle.decode(usersdata)
        session.pop('usersdata')

    # filter users bassed on form fields data
    if request.method == 'POST':
        form = UserSearchForm(request.form)
        if (form.first_name.data):
            users = list(filter(lambda u: form.first_name.data in u.first_name, users))
        if (form.last_name.data):
            users = list(filter(lambda u: form.last_name.data in u.last_name, users))
        if (form.email.data):
            users = list(filter(lambda u: form.email.data in u.email, users))
        if (int(form.role.data) != 0):
            users = list(filter(lambda u: int(form.role.data) == u.role, users))
        
        session['formdata'] = request.form
        session['usersdata'] = jsonpickle.encode(users)
        return redirect(url_for('profile.manage'))
    return render_template('profile/manage.html', \
        users=users, user_form=UserForm(), user_search_form=user_search_form)


@profile.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        email_exists = User.query.filter_by(email=form.data['email']).first()
        if (not email_exists):
            user = User(_first_name=form.data['first_name'],
                        _last_name=form.data['last_name'],
                        _email=form.data['email'],
                        _role=UserRole(int(form.data['role'])).value,
                        # only developers know password :D
                        _password='testpassword')
            print(user.role)
            db.session.add(user)
            db.session.commit()
            return jsonify(status=200, message='User successfully created.')
        return jsonify(status=500, message='User with this email already exists!')
    else:
        # return render_template('profile/manage.html', user_form=form)
        return jsonify(status=500, message='Some fields are missing or incorrect!')


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
    
    if (user.role == UserRole.DIRECTOR.value):
        # if director is deleted, admin becomes hotel owner :)
        admin = User.query.filter_by(role=UserRole.ADMIN.value).first()
        director_hotels = Hotel.query.filter_by(owner=user).all()
        admin.own_hotels.extend(director_hotels)
        db.session.add(admin)

    user.is_active = False
    db.session.add(user)
    db.session.commit()
    return jsonify(status=200, message='User successfully deleted.')