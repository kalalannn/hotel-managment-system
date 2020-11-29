from flask import request, render_template, session, redirect, url_for, flash, json, jsonify

from flask_login import current_user, login_user, logout_user, login_required

from . import hotels
from .forms import SearchForm, HotelForm
from .forms import RoomForm, RoomCategoryForm
from ..forms import SubmitForm
from ..models import Hotel, Address, User, HotelStars, UserRole
from ..models import Room, RoomCategory, RoomType
from app import db
from app.helpers import Helper

@hotels.route('/list', methods=['GET', 'POST'])
@hotels.route('/list/<int:owner_id>', methods=['GET', 'POST'])
def list(owner_id=None):
    form = SearchForm(request.form)

    query = Hotel.query
    if owner_id:
        query = query.filter(Hotel.owner_id == owner_id)

    # POST
    if form.validate_on_submit():

        if form.name.data is not None:
            query = query.filter(Hotel.name.like("%{}%".format(form.name.data)))

        # if form.stars.data:
        #     query = query.filter(Hotel.stars == form.stars.data.value)
    else:
        query = query.order_by(Hotel.stars).limit(10)
    
    hotels = query.all()
    return render_template('hotels/list.html', form=form, hotels=hotels)

@hotels.route('/new/', methods=['GET', 'POST'])          # Only admin
@hotels.route('/edit/<int:hotel_id>', methods=['GET', 'POST']) # Director+
@login_required
def update(hotel_id=None):
    if hotel_id:
        hotel   = Hotel.query.filter_by(id=hotel_id).one()
        form    = HotelForm(request.form, obj=hotel)
    else:
        hotel   = None
        form    = HotelForm(request.form)

    if not ((current_user.role == UserRole.DIRECTOR.value
                and hotel_id
                and current_user == hotel.owner)
            or (current_user.role  == UserRole.ADMIN.value)):
        return redirect(url_for('forbidden'))

    if current_user.role == UserRole.ADMIN.value:
        form.admin()
    elif current_user.role == UserRole.DIRECTOR.value:
        form.director()

    if form.validate_on_submit():
        if current_user.role == UserRole.ADMIN.value:
            address = Address(form.address_country.data, form.address_city.data, \
                form.address_post_code.data, form.address_street.data, \
                form.address_number.data)
        # EDIT
        if hotel_id:
            if current_user.role == UserRole.ADMIN.value:
                hotel.name = form.name.data
                hotel.stars = form.stars.data.value
                hotel.address = address
                hotel.owner = form.owner.data

            hotel.description = form.description.data
        # NEW
        elif current_user.role == UserRole.ADMIN.value:
            db.session.add(address)
            hotel = Hotel(
                form.name.data,
                form.description.data,
                form.stars.data.value,
                address,
                form.owner.data,
                # owner
            )
            db.session.add(hotel)
        db.session.commit()
        return redirect(url_for('hotels.list'))

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

    return jsonify([i.serialize for i in query.all()])

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

    return jsonify([i.serialize for i in query.all()])

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
    hotel = Hotel.query.filter_by(id=hotel_id).one()
    return render_template('hotels/update.html',
        op='Show', hotel=hotel)

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
