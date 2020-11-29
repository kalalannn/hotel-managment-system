from flask import request, render_template, session, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from . import users
from .forms import LoginForm, RegistrationForm, NewPasswordForm, UserForm, UserSearchForm
from ..models import User, UserRole, Hotel
from app import db

import jsonpickle

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('users.home'))
        flash('Invalid username or password.', 'error')
    return render_template('users/login.html', form=form)


@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if current_user.is_authenticated and current_user.role == UserRole.ADMIN.value:
        form.admin()
    elif current_user.is_authenticated and current_user.role == UserRole.DIRECTOR.value:
        form.director()
    else:
        form.others()

    # POST
    if form.validate_on_submit():
        if current_user.is_authenticated and current_user.role >= UserRole.DIRECTOR.value:
            role = form.role.data
        else:
            role = UserRole.CUSTOMER.value

        user = User(form.first_name.data,
                    form.last_name.data,
                    form.email.data,
                    form.password.data,
                    role)
        db.session.add(user)
        db.session.commit()
        if current_user.is_authenticated and current_user.role >= UserRole.DIRECTOR.value:
            flash('User {} was created'.format(user.email))
            return redirect (url_for('users.manage'))
        else:
            flash('You can now log in.')
            return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


@users.route('/new_password', methods=['GET', 'POST'])
@login_required
def new_password():
    form = NewPasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.password = form.new_password.data
            db.session.commit()
            logout_user()
            flash('You can now log in with a new password.', 'info')
            return redirect(url_for('users.login'))
        flash('You entered wrong current password.', 'error')
    return render_template('users/new_password.html', form=form)


@users.route('/home/', methods=['GET'])
def home():
    return render_template('users/home.html')



@users.route('/manage', methods=['GET', 'POST'])
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
        return redirect(url_for('users.manage'))
    return render_template('users/manage.html', \
        users=users, user_form=UserForm(), user_search_form=user_search_form)


@users.route('/add_user', methods=['GET', 'POST'])
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
            db.session.add(user)
            db.session.commit()
            return jsonify(status=200, message='User successfully created.')
        return jsonify(status=500, message='User with this email already exists!')
    else:
        # return render_template('users/manage.html', user_form=form)
        return jsonify(status=500, message='Some fields are missing or incorrect!')


@users.route('/edit_user/<id>', methods=['GET', 'POST'])
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


@users.route('/delete_user/<id>', methods=['GET'])
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