from flask import request, render_template, session, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required

from . import users
from .forms import LoginForm, UserForm, EditUserForm, NewPasswordForm, UserSearchForm
from ..forms import SubmitForm
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
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@users.route('/new_or_update_user', methods=['POST'])
@users.route('/new_or_update_user/<int:user_id>', methods=['GET', 'POST'])
def new_or_update_user(user_id=None):
    user = None
    if user_id:
        user = User.First(user_id)
        if user:
            form = EditUserForm(request.form, obj=user)
        else:
            return redirect(url_for('error'))
    else:
        form = UserForm(request.form)

    if current_user.is_authenticated:
        if current_user.role == UserRole.ADMIN.value:
            form.admin()
        elif current_user.role == UserRole.DIRECTOR.value:
            form.director()
        else:
            return redirect(url_for('forbidden'))
    else:
        form.anon()

    # print(form.data)
    # print(request.form)

    # POST
    if form.validate_on_submit():
        if current_user.is_authenticated:
            if current_user.role == UserRole.DIRECTOR.value \
                and int(form.role.data) not in [UserRole.CUSTOMER.value, UserRole.RECEPTIONIST.value]:
                return redirect(url_for('forbidden'))
            role = int(form.role.data)
        else:
            role = UserRole.CUSTOMER.value

        # TODO opravneni!!
        if user_id:
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.role = role
            db.session.commit()
            flash('User {} {} was updated'.format(user.first_name, user.last_name), 'info')
        else:
            user = User.New(form.first_name.data,
                            form.last_name.data,
                            form.email.data,
                            form.password.data,
                            role)
            flash('User {} {} was created. Now you can log in.'.format(user.first_name, user.last_name), 'info')

        if current_user.is_authenticated:
            if current_user.role >= UserRole.DIRECTOR.value:
                # To reload usersdata
                if session.get('usersdata'):
                    session.pop('usersdata')

    elif request.method == 'POST':
        flash('Wrong Form! {}'.format(form.errors), 'error')

    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect (url_for('users.manage'))
        else:
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
            flash('Now you can log in with a new password.', 'info')
            return redirect(url_for('users.login'))
        flash('Wrong current password!', 'error')
    else:
        flash('Wrong Form!', 'error')
    return render_template('users/new_password.html', form=form)


@users.route('/home/', methods=['GET'])
def home():
    return render_template('users/home.html')

# TODO Opravneni
@users.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.First(user_id)
    if user:
        return jsonify(user.serialize)
    else:
        return (404, 'Not Found')

@users.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    search_form = UserSearchForm(obj=request.form)

    # session.pop('formdata')
    # session.pop('usersdata')

    if current_user.role == UserRole.ADMIN.value:
        search_form.admin()
    elif current_user.role == UserRole.DIRECTOR.value:
        search_form.director()
    else:
        return redirect(url_for('forbidden'))

    query = None
    if current_user.role == UserRole.DIRECTOR.value:
        query = User.query.join(Hotel, User.recept_hotels).filter(Hotel.id.in_([h.id for h in current_user.own_hotels]))
        # TODO Customers, that have done reservations (not edit, not delete)

    if search_form.validate_on_submit():
        users = User.All(query, search_form.first_name.data, search_form.last_name.data, search_form.email.data, search_form.role.data)
        
        # print ("save formdata {}".format(request.form))
        # formdata reload
        if session.get('formdata'):
            session.pop('formdata')
        session['formdata'] = request.form

        # usersdata reload
        if session.get('usersdata'):
            session.pop('usersdata')
        session['usersdata'] = jsonpickle.encode(users)

        return redirect(url_for('users.manage'))

    if (session.get('formdata')):
        formdata = session.get('formdata')
        # print ("load formdata {}".format(formdata))
        # WARNING: not replace csrf_token!!
        search_form.first_name.data = formdata['first_name']
        search_form.last_name.data  = formdata['last_name']
        search_form.email.data      = formdata['email']
        search_form.role.data       = int(formdata['role'])

    if (session.get('usersdata')):
        usersdata = session.get('usersdata')
        # print ("load userdata {}".format(usersdata))
        users = jsonpickle.decode(usersdata)
    else:
        users = User.All(query, search_form.first_name.data, search_form.last_name.data, search_form.email.data, search_form.role.data)

    new_form = UserForm()
    edit_form = EditUserForm()
    if current_user.is_authenticated and current_user.role == UserRole.ADMIN.value:
        new_form.admin()
        edit_form.admin()
    elif current_user.is_authenticated and current_user.role == UserRole.DIRECTOR.value:
        new_form.director()
        edit_form.director()
    else:
        new_form.anon()
        edit_form.anon()

    return render_template('users/manage.html',
        users=users, search_form=search_form, new_form=new_form, edit_form=edit_form, submit_form=SubmitForm())

@users.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete(user_id):
    form = SubmitForm(request.form)

    user = User.First(user_id)
    if not user:
        flash('Wrong user!', 'error')
        return redirect(url_for('users.manage'))

    if form.validate_on_submit():
        if (user.role == UserRole.ADMIN.value):
            flash('Cannot delete admin!', 'error')
            return redirect(url_for('users.manage'))
        if (user.id == current_user.id):
            flash('Cannot delete current user!', 'error')
            return redirect(url_for('users.manage'))
        
        if (user.role == UserRole.DIRECTOR.value):
            # if director is deleted, admin becomes hotel owner :)
            admin = User.query.filter_by(role=UserRole.ADMIN.value).first()
            director_hotels = Hotel.query.filter_by(owner=user).all()
            admin.own_hotels.extend(director_hotels)

        user.is_active = False
        db.session.commit()
        if session.get('usersdata'):
            session.pop('usersdata')
        flash('User {} {} was deactivated.'.format(user.first_name, user.last_name), 'info')
    else:
        flash('Wrong form!', 'error')

    return redirect(url_for('users.manage'))