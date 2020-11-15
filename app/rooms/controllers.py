from flask import request, render_template, session, redirect, url_for, flash, json
from . import rooms
from .forms import RoomForm, RoomCategoryForm
from ..models import Hotel, Address, User, HotelStars, UserRole, Room, RoomCategory
from app import db
from app.helpers import Helper

@rooms.route('/new/<int:hotel_id>', methods=['GET', 'POST'])
def new(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).one()
    room_form = RoomForm(request.form, obj=hotel)
    room_form.add_room()

    if room_form.validate_on_submit():
        for i in range(int(room_form.numbers_from.data), int(room_form.numbers_to.data)+1):
            room = Room(i, room_form.number_of_beds.data, room_form.room_category.data)
            db.session.add(room)
        db.session.commit()
        return redirect(url_for('rooms.new', hotel_id=hotel_id))
    return render_template('rooms/new_room.html', form=room_form, hotel=hotel)

@rooms.route('/new_category/<int:hotel_id>', methods=['GET', 'POST'])
def new_category(hotel_id):
    hotel = Hotel.query.filter_by(id=hotel_id).one()
    category_form = RoomCategoryForm(request.form, obj=hotel)
    category_form.addCategory()

    if category_form.validate_on_submit():
        hotel = Hotel.query.filter_by(id=hotel_id).one()
        category = RoomCategory(category_form.category.data.type, int(category_form.category_price.data), hotel)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('rooms.new_category', hotel_id=hotel_id))
    return render_template('rooms/new_category.html', form=category_form, hotel=hotel)
