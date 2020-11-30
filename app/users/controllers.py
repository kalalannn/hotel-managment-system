from flask import request, render_template, session, redirect, url_for, flash, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from ..permissions import role_required

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


@users.route('/find_user', methods=['GET'])
def find_user():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    return jsonify(
        {'first_name': user.first_name,
        'last_name': user.last_name})


@users.route('/get_or_create_user', methods=['GET', 'POST'])
def get_or_create_user():
    data = request.get_json()
    email = data['email']
    first_name = data['first_name']
    last_name = data['last_name']

    user = User.query.filter_by(email=email).first()
    # if no user found in database, create ANON
    if not user:
        user = User(_first_name=first_name,
            _last_name=last_name,
            _email=email,
            _role=UserRole.ANON.value)
        db.session.add(user)
        db.session.commit()

    return jsonify({'user_id': user.id})


@users.route('/new_or_update_user', methods=['GET', 'POST'])
@users.route('/new_or_update_user/<int:user_id>', methods=['GET', 'POST'])
def new_or_update_user(user_id=None):
    user = None
    if user_id:
        user = User.by_ids(User.subordinates_editable(User.query, current_user), [user_id]).first()
        if user:
            form = EditUserForm(request.form, obj=user)
        else:
            return redirect(url_for('forbidden'))
    else:
        form = UserForm(request.form)

    if current_user.is_authenticated:
        if current_user.role == UserRole.ADMIN.value:
            form.admin()
        elif current_user.role == UserRole.DIRECTOR.value:
            form.director(current_user)
        else:
            form.anon()
    else:
        form.anon()

    # POST
    if form.validate_on_submit():
        # Not Present in UserForm neither EditUserForm
        if user:
            is_active = user.is_active
        else:
            is_active = True

        if form.role and int(form.role.data) != 0:
            role = int(form.role.data)
        elif user:
            role = user.role
        else: # AnonMixin want to register
            role = UserRole.CUSTOMER.value

        # Can Be present in UserForm or EditUserForm
        if form.recept_hotel_id and int(form.recept_hotel_id.data) != 0:
            recept_hotels = Hotel.by_ids(Hotel.subordinates_editable(Hotel.query, current_user), [int(form.recept_hotel_id.data)]).first()
            if not recept_hotels:
                return redirect(url_for('forbidden'))
        elif user:
            recept_hotels = user.recept_hotels
        else:
            recept_hotels = None

        ok, err = User.can_write(current_user, user,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                role,
                is_active,
                recept_hotels)
        if not ok:
            print ('Permission ERROR: '+ err)
            # flash(err, 'error') # REMOVE, need to log!
            return redirect(url_for('forbidden'))

        if user: # Edit
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            user.role = role
            flash('User {} {} was updated'.format(user.first_name, user.last_name), 'info')
        else: # New
            user = User.new(form.first_name.data,
                            form.last_name.data,
                            form.email.data,
                            form.password.data,
                            role,
                            True,
                            recept_hotels)
            flash('User {} {} was created. Now you can log in.'.format(user.first_name, user.last_name), 'info')
        db.session.commit()

        if current_user.is_authenticated:
            if current_user.role >= UserRole.DIRECTOR.value:
                # To reload usersdata
                if session.get('usersdata'):
                    session.pop('usersdata')
    elif request.method == 'POST':
        flash('Wrong Form! {}'.format(form.errors), 'error')
        if current_user.is_authenticated:
            # TODO CUST + others
            return redirect (url_for('users.manage'))
        else:
            return redirect(url_for('users.new_or_update_user'))

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
    user = User.by_ids(User.subordinates_editable(User.query, current_user), [user_id]).first()
    if user:
        return jsonify(user.serialize)
    else:
        return (404, 'Not Found')

@users.route('/manage', methods=['GET', 'POST'])
@role_required(UserRole.ADMIN, UserRole.DIRECTOR)
def manage():
    search_form = UserSearchForm(obj=request.form)

    # session.pop('formdata')
    # session.pop('usersdata')

    query = User.subordinates_editable(User.query, current_user)
    if search_form.validate_on_submit():
        query = User.filter(query, search_form.first_name.data, search_form.last_name.data, search_form.email.data, search_form.role.data)
        users = query.all()
        
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
        users = User.filter(query, search_form.first_name.data, search_form.last_name.data, search_form.email.data, search_form.role.data)

    new_form = UserForm()
    edit_form = EditUserForm()
    if current_user.is_authenticated and current_user.role == UserRole.ADMIN.value:
        new_form.admin()
        edit_form.admin()
    elif current_user.is_authenticated and current_user.role == UserRole.DIRECTOR.value:
        new_form.director(current_user)
        edit_form.director(current_user)
    else:
        new_form.anon()
        edit_form.anon()

    return render_template('users/manage.html',
        users=users, search_form=search_form, new_form=new_form, edit_form=edit_form, submit_form=SubmitForm())

@users.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete(user_id):
    form = SubmitForm(request.form)

    # TODO opravneni

    user = User.by_ids(User.subordinates_editable(User.query, current_user), [user_id]).first()
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