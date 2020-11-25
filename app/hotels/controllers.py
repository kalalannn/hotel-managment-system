from flask import request, render_template, session, redirect, url_for, flash, json, make_response

from flask_login import current_user, login_user, logout_user, login_required
import datetime
from . import hotels
from .forms import SearchForm, HotelForm
from .forms import RoomForm, RoomCategoryForm
from ..reservations.forms import ReservationForm
from ..models import Hotel, Address, User, HotelStars, UserRole, Reservation, Payment, ReservationRoom
from ..models import Room, RoomCategory, RoomType
from app import db
from app.helpers import Helper

@hotels.route('/list/', methods=['GET', 'POST'])
def list():
    form = SearchForm(request.form)

    _hotels = None
    if request.method == 'GET':
        _hotels = Hotel.query.order_by(Hotel.stars).limit(10).all()
    # POST
    elif form.validate_on_submit():
        query = Hotel.query

        if form.name.data is not None:
            query = query.filter(Hotel.name.like("%{}%".format(form.name.data)))

        # if form.stars.data:
        #     query = query.filter(Hotel.stars == form.stars.data.value)

        _hotels = query.all()
    # EMPTY FORM
    else:
        _hotels = Hotel.query.limit(10).all()

    resp = make_response(render_template('hotels/list.html', form=form, hotels=_hotels), )
    resp.set_cookie('date_from', '2020-02-02')
    resp.set_cookie('date_to', '2020-03-03')
    return resp
    #return render_template('hotels/list.html', form=form, hotels=_hotels)

@login_required
@hotels.route('/new/', methods=['GET', 'POST'])          # Only admin
@hotels.route('/edit/<int:hotel_id>', methods=['GET', 'POST']) # Director+
def update(hotel_id=None):
    if hotel_id:
        op      = 'Edit'
        hotel   = Hotel.query.filter_by(id=hotel_id).one()
        form    = HotelForm(request.form, obj=hotel)
    else:
        op      = 'New'
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
            op=op, form=form, hotel=hotel, room_form=room_form, category_form=category_form)
    else:
        return render_template('hotels/update.html', \
            op=op, form=form)

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
            int(form.price.data), hotel)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('hotels.update', hotel_id=hotel_id))
    else:
        return redirect (url_for('error', error="Wrong data."))

# There must be hotel_id to SHOW!
@hotels.route('/show/<int:hotel_id>', methods=['GET', 'POST'])
def show(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).one()
    date_from = request.cookies.get('date_from')
    date_to = request.cookies.get('date_to')
    if current_user.is_authenticated:
        form = ReservationForm(request.form, obj=hotel, date_from=date_from, date_to=date_to, user=current_user)
        form.authorised()
    else:
        form = ReservationForm(request.form, obj=hotel, date_from=date_from, date_to=date_to)
        form.unauthorised()
    if form.validate_on_submit():
        room_category = RoomCategory.query.filter_by(hotel_id=hotel.id, type=form.category.data.type).one()
        amount = room_category.price
        payment = Payment(amount//2, amount, 0.1,False, False)
        df= datetime.datetime.strptime(str(form.date_from.data), '%Y-%m-%d')
        dt= datetime.datetime.strptime(str(form.date_to.data), "%Y-%m-%d")
        reservation_room = ReservationRoom(df, dt)
        reservation = Reservation('CREATED', current_user, current_user, payment)
        db.session.add(reservation)
        db.session.commit()
        if (room_category.type == 'STANDARD'):
            b = form.beds_1.data
            beds = int(b.beds)
        elif (room_category.type == "LUX"):
            b = form.beds_2.data
            beds = int(b.beds)
        else:
            b = form.beds_3.data
            beds = int(b.beds)
        room = Room.query.filter_by(room_category_id=room_category.id, beds=beds).one()
        reservation_room.room_id = room.id
        reservation_room.reservation_id = reservation.id
        db.session.add(reservation_room)
        db.session.commit()
    return render_template('hotels/show.html', hotel=hotel, form=form)

# # There also
# @hotels.route('/edit/', methods=['GET', 'POST'])
# def edit():
#     return render_template('hotels/edit.html')