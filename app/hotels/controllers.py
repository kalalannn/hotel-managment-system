from flask import request, render_template, session, redirect, url_for, flash, json, jsonify, make_response

from flask_login import current_user, login_user, logout_user, login_required
from ..permissions import role_required

from . import hotels
from .forms import SearchForm, HotelForm
from .forms import RoomForm, RoomCategoryForm
from ..reservations.forms import UserForm as ReservationForm
from ..forms import SubmitForm
from ..models import Hotel, Address, User, HotelStars, UserRole
from ..models import Room, RoomCategory, RoomType
from app import db
from app.helpers import Helper


# @hotels.route('setcookie', methods=['GET', 'POST'])
# def setcookie():
#     if request.method == 'POST':
#         name = request.form['name']
#     print(name)
#     return redirect(url_for('hotels.hotel_list'))


@hotels.route('/list', methods=['GET', 'POST'])
@hotels.route('/list/<int:owner_id>', methods=['GET', 'POST'])
def hotel_list(owner_id=None):
    form = SearchForm(request.form)

    query = Hotel.query.join(Address, Hotel.address)
    if owner_id:
        query = Hotel.subordinates_editable(Hotel.query, current_user)
    # POST
    if form.validate_on_submit():
        if form.name.data is not None:
            query = Hotel.filter(query, name=form.name.data)
        if form.country.data is not None:
            query = Address.filter(query, country=form.country.data.country)
        if form.date_from.data and form.date_to.data:
            # TODO
            free_rooms = Room.free_rooms_by_dates(form.date_from.data, form.date_to.data)
    else:
        query = query.order_by(Hotel.stars).limit(10)

    hotels = query.all()

    resp = make_response(render_template('hotels/list.html', form=form, hotels=hotels))

    if form.validate_on_submit():
        # date_from = '-'.join(list(reversed(str(form.date_from.data).split('-'))))
        # date_to = '-'.join(list(reversed(str(form.date_to.data).split('-'))))
        resp.set_cookie('date_from', str(form.date_from.data))
        resp.set_cookie('date_to', str(form.date_to.data))
        # resp.set_cookie('date_from', date_from)
        # resp.set_cookie('date_to', date_to)

    return resp

@hotels.route('/new/', methods=['GET', 'POST'])          # Only admin
@hotels.route('/edit/<int:hotel_id>', methods=['GET', 'POST']) # Director+
@role_required(UserRole.ADMIN, UserRole.DIRECTOR)
def update(hotel_id=None):
    if hotel_id:
        hotel = Hotel.by_ids(Hotel.subordinates_editable(Hotel.query, current_user), [hotel_id]).first()
        form    = HotelForm(request.form, obj=hotel)
        op = 'Edit'
        if not hotel:
            return redirect(url_for('forbidden'))
    else:
        hotel   = None
        form    = HotelForm(request.form)
        op = 'New'


    if current_user.role == UserRole.ADMIN.value:
        form.admin()
    elif current_user.role == UserRole.DIRECTOR.value:
        form.director()

    if form.validate_on_submit():
        # if current_user.role == UserRole.ADMIN.value:
        address = Address(form.address_country.data, form.address_city.data, \
            form.address_post_code.data, form.address_street.data, \
            form.address_number.data)

        if current_user.role == UserRole.ADMIN.value:
            owner = int(form.owner.data)
        elif hotel:
            owner = hotel.owner
        else:
            owner = current_user

        # EDIT
        if hotel_id:
            hotel.name = form.name.data
            hotel.stars = form.stars.data.value
            db.session.delete(hotel.address)
            hotel.address = address
            hotel.owner = owner
            hotel.description = form.description.data
        # NEW
        else:
            hotel = Hotel(
                form.name.data,
                form.description.data,
                form.stars.data.value,
                address,
                owner,
            )
            db.session.add(hotel)
        address.hotel_id = hotel.id
        db.session.add(address)
        db.session.commit()
        return redirect(url_for('hotels.hotel_list'))

    if hotel_id:
        room_form       = RoomForm(hotel_id=hotel_id)
        category_form   = RoomCategoryForm()
        submit_form     = SubmitForm()
        # In template you already has this
        # rooms           = hotel.room_categories.rooms
        # room_categories = hotel.room_categories
        return render_template('hotels/update.html', \
            op='Edit', form=form, hotel=hotel, room_form=room_form, category_form=category_form, submit_form=submit_form)
    else:
        return render_template('hotels/update.html', \
            op='New', form=form)

@hotels.route('/room_categories', methods=['GET'])
@hotels.route('/room_categories/<int:room_category_id>', methods=['GET'])
@hotels.route('<int:hotel_id>/room_categories', methods=['GET'])
@hotels.route('<int:hotel_id>/room_categories/<int:room_category_id>', methods=['GET'])
def get_room_categories(hotel_id=None, room_category_id=None):
    query = RoomCategory.query.join(Hotel, RoomCategory.hotel)
    if hotel_id:
        query = query.filter(Hotel.id == hotel_id)

    if room_category_id:
        query = query.filter(RoomCategory.id == room_category_id)

    return jsonify([i.serialize() for i in query.all()])

@hotels.route('/rooms', methods=['GET'])
@hotels.route('/rooms/<int:room_id>', methods=['GET'])
@hotels.route('/room_categories/<int:room_category_id>/rooms', methods=['GET'])
@hotels.route('<int:hotel_id>/rooms', methods=['GET'])
@hotels.route('<int:hotel_id>/room_categories/<int:room_category_id>/rooms', methods=['GET'])
@hotels.route('<int:hotel_id>/room_categories/<int:room_category_id>/rooms/<int:room_id>', methods=['GET'])
def get_rooms(hotel_id=None, room_category_id=None, room_id=None):
    query = Room.query.join(RoomCategory, Room.room_category).join(Hotel, RoomCategory.hotel)
    if hotel_id:
        query = query.filter(Hotel.id == hotel_id)

    if room_category_id:
        query = query.filter(RoomCategory.id == room_category_id)

    if room_id:
        query = query.filter(Room.id == room_id)

    return jsonify([i.serialize() for i in query.all()])

@hotels.route('/<int:hotel_id>/rooms/new', methods=['POST'])
@hotels.route('/<int:hotel_id>/rooms/<int:room_id>', methods=['POST'])
@login_required
def new_or_update_room(hotel_id, room_id=None):
    hotel = Hotel.query.filter_by(id=hotel_id).one()
    if not hotel:
        return redirect (url_for('error', error="Can not find hotel."))

    if not ((current_user.role == UserRole.DIRECTOR.value
                and hotel_id
                and current_user == hotel.owner)
            or (current_user.role  == UserRole.ADMIN.value)):
        return redirect(url_for('forbidden'))

    if room_id:
        room = Room.query.filter_by(id=room_id).first()
        form = RoomForm(request.form, obj=room)
    else:
        form = RoomForm(request.form, hotel_id=hotel_id)

    if form.validate_on_submit():
        if room_id:
            # print("Room Update hotel_id: {}, room_id: {}".format(hotel_id, room_id))
            room.number = form.number.data
            room.beds = form.beds.data
            room.room_category = form.room_category.data
        else:
            room = Room(form.number.data, form.beds.data, form.room_category.data)
            db.session.add(room)
        db.session.commit()
        return redirect(url_for('hotels.update', hotel_id=hotel_id))
    else:
        return redirect (url_for('error'))

@hotels.route('/<int:hotel_id>/room_categories/new', methods=['POST'])
@hotels.route('/<int:hotel_id>/room_categories/<int:room_category_id>', methods=['POST'])
@login_required
def new_or_update_room_category (hotel_id, room_category_id=None):
    hotel = Hotel.query.filter_by(id=hotel_id).one()
    if not hotel:
        return redirect (url_for('error'))

    if not ((current_user.role == UserRole.DIRECTOR.value and current_user == hotel.owner)
            or (current_user.role  == UserRole.ADMIN.value)):
        return redirect(url_for('forbidden'))

    if room_category_id:
        room_category = RoomCategory.query.filter_by(id=room_category_id).first()
        form = RoomCategoryForm(request.form, obj=room_category)
    else:
        form = RoomCategoryForm(request.form, hotel_id=hotel_id)

    if form.validate_on_submit():
        if room_category_id:
            # print("RoomCategory Update hotel_id: {}, room_category_id: {}".format(hotel_id, room_category_id))
            room_category.type = form.type.data.value
            room_category.price = float(form.price.data)
            room_category.description = form.description.data
        else:
            room_category = RoomCategory(form.type.data.value, \
                float(form.price.data), hotel, form.description.data)
            db.session.add(room_category)
        db.session.commit()
        return redirect(url_for('hotels.update', hotel_id=hotel_id))
    else:
        return redirect (url_for('error', error="Wrong data."))

@hotels.route('/show/<int:hotel_id>', methods=['GET'])
def show(hotel_id):
    date_from = request.cookies.get('date_from')
    date_to = request.cookies.get('date_to')
    hotel = Hotel.by_ids(Hotel.query, [hotel_id]).first()
    dates = {'date_from': date_from, 'date_to': date_to}
    reservation_form = ReservationForm(dates=dates)
    if current_user.is_authenticated:
        reservation_form.registered()
    return render_template('hotels/update.html',
        op='Show', hotel=hotel, reservation_form=reservation_form)


@hotels.route('/delete/<int:hotel_id>', methods=['POST'])
@hotels.route('/delete/room_category/<int:room_category_id>', methods=['POST'])
@hotels.route('/delete/room/<int:room_id>', methods=['POST'])
@login_required
def delete(hotel_id=None, room_category_id=None, room_id=None):
    # TODO
    if not ((current_user.role == UserRole.DIRECTOR.value
                and hotel_id
                and current_user == hotel.owner)
            or (current_user.role  == UserRole.ADMIN.value)):
        return redirect(url_for('forbidden'))

    form = SubmitForm(request.form)
    if form.validate_on_submit():
        if hotel_id:
            # TODO
            pass
        elif room_category_id:
            # TODO
            pass
        elif room_id:
            room = Room.query.filter(Room.id == room_id).first()
            hotel_id = room.room_category.hotel_id
            if room:
                db.session.delete(room)
            else:
                return redirect('error')
        else:
            return redirect('error')
        db.session.commit()
    else:
        return redirect(url_for('error'))

    return redirect(url_for('hotels.update', hotel_id=hotel_id))
