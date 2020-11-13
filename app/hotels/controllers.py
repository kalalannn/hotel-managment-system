from flask import request, render_template, session, redirect, url_for, flash, json

from flask_login import current_user, login_user, logout_user, login_required

from . import hotels
from .forms import SearchForm, HotelForm, AddRoomForm
from ..models import Hotel, Address, User, HotelStars, UserRole, Room
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

        if form.stars.data:
            query = query.filter(Hotel.stars == form.stars.data.value)

        _hotels = query.all()
    # EMPTY FORM
    else:
        _hotels = Hotel.query.limit(10).all()

    return render_template('hotels/list.html', form=form, hotels=_hotels)

@login_required
@hotels.route('/new/', methods=['GET', 'POST'])          # Only admin
@hotels.route('/edit/<int:hotel_id>', methods=['GET', 'POST']) # Director+
def update(hotel_id=None):
<<<<<<< HEAD
    form = HotelForm(request.form, obj=None)
    add_room_form = AddRoomForm(request.form, obj=None)
=======
    form = HotelForm(request.form)
>>>>>>> main
    hotel = None

    if hotel_id:
        op = 'Edit'
        hotel = Hotel.query.filter_by(id=hotel_id).one()
        form = HotelForm(request.form, obj=hotel)
        add_room_form =  AddRoomForm(request.form, obj=hotel)

        if current_user.role == UserRole.ADMIN.value:
            form.admin()
        elif current_user.role == UserRole.DIRECTOR.value and current_user == hotel.owner:
            add_room_form =  AddRoomForm(request.form, obj=hotel)
            form.director()
            add_room_form.add_room()
        else:
            return redirect(url_for('forbidden'))
    elif current_user.role == UserRole.ADMIN.value:
        op = 'New'
        form.admin()
    else:
        return redirect(url_for('forbidden'))


    if add_room_form.validate_on_submit():
        for i in range(int(add_room_form.numbers_from.data), int(add_room_form.numbers_to.data)+1):
            room = Room(i, add_room_form.number_of_beds.data, add_room_form.room_category.data)
            db.session.add(room)
        db.session.commit()
    # Now form is ready

    # POST (DIRECTOR + ADMIN)
    elif form.validate_on_submit():
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


    rooms = Room.query.filter_by(room_category=add_room_form.room_category.data).all()
    return render_template('hotels/update.html', form=form, rooms=rooms, hotel=hotel, op=op, add_room_form=add_room_form)

# There must be hotel_id to SHOW!
# @hotels.route('/show/', methods=['GET', 'POST'])
# def show():
#     return render_template('hotels/show.html')

# # There also
# @hotels.route('/edit/', methods=['GET', 'POST'])
# def edit():
#     return render_template('hotels/edit.html')