from flask import request, render_template, session, redirect, url_for, flash, json

from flask_login import current_user, login_user, logout_user, login_required

from . import hotels
from .forms import SearchForm, HotelForm
from .forms import RoomForm, RoomCategoryForm
from ..models import Hotel, Address, User, HotelStars, UserRole
from ..models import Room, RoomCategory, RoomType
from app import db
from app.helpers import Helper

@hotels.route('/list/', methods=['GET', 'POST'])
def list():
    form = SearchForm(request.form)

    hotels = None
    if request.method == 'GET':
        hotels = Hotel.query.order_by(Hotel.stars).limit(10).all()
    # POST
    elif form.validate_on_submit():
        query = Hotel.query

        if form.name.data is not None:
            query = query.filter(Hotel.name.like("%{}%".format(form.name.data)))

        # if form.stars.data:
        #     query = query.filter(Hotel.stars == form.stars.data.value)

        hotels = query.all()
    # EMPTY FORM
    else:
        hotels = Hotel.query.order_by(Hotel.stars).limit(10).all()

    return render_template('hotels/list.html', form=form, hotels=hotels)

@login_required
@hotels.route('/new/', methods=['GET', 'POST'])          # Only admin
@hotels.route('/edit/<int:hotel_id>', methods=['GET', 'POST']) # Director+
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
        # In template you already has this
        # rooms           = hotel.room_categories.rooms
        # room_categories = hotel.room_categories
        return render_template('hotels/update.html', \
            op='Edit', form=form, hotel=hotel, room_form=room_form, category_form=category_form)
    else:
        return render_template('hotels/update.html', \
            op='New', form=form)

@login_required
@hotels.route('/<int:hotel_id>/room_categories/rooms/new', methods=['POST'])
def new_room_category_rooms(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).one()
    if not hotel:
        return redirect (url_for('error', error="Can not find hotel."))

    if not ((current_user.role == UserRole.DIRECTOR.value
                and hotel_id
                and current_user == hotel.owner)
            or (current_user.role  == UserRole.ADMIN.value)):
        return redirect(url_for('forbidden'))

    form = RoomForm(request.form, hotel_id=hotel_id)
    if form.validate_on_submit():
        _from = int(form.numbers_from.data)
        _to   = int(form.numbers_to.data) + 1
        for i in range(_from,_to):
            room = Room(i, form.beds.data, form.room_category.data)
            db.session.add(room)
        db.session.commit()
        return redirect(url_for('hotels.update', hotel_id=hotel_id))
    else:
        return redirect (url_for('error'))

@login_required
@hotels.route('/<int:hotel_id>/room_categories/new', methods=['POST'])
def new_room_category (hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).one()
    if not hotel:
        return redirect (url_for('error'))

    if not ((current_user.role == UserRole.DIRECTOR.value
                and hotel_id
                and current_user == hotel.owner)
            or (current_user.role  == UserRole.ADMIN.value)):
        return redirect(url_for('forbidden'))

    form = RoomCategoryForm(request.form, hotel_id=hotel_id)
    if form.validate_on_submit():
        category = RoomCategory(RoomType(form.type.data).name, \
            int(form.price.data), hotel, form.description.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('hotels.update', hotel_id=hotel_id))
    else:
        return redirect (url_for('error', error="Wrong data."))

@hotels.route('/show/<int:hotel_id>', methods=['GET'])
def show(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).one()
    return render_template('hotels/update.html',
        op='Show', hotel=hotel)

# # There also
# @hotels.route('/edit/', methods=['GET', 'POST'])
# def edit():
#     return render_template('hotels/edit.html')