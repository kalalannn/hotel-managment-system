from flask import request, render_template, jsonify, json, flash, redirect, url_for
from flask_login import current_user
from datetime import datetime, date
from decimal import Decimal
import uuid

import jsonpickle

from . import reservations
# Import needed forms and models
from .forms import UserForm, StatusForm
from ..forms import SubmitForm
from ..models import User, UserRole, Hotel, Room, RoomCategory, ReservationRoom, ReservationStatus, \
    RoomType, Payment, History, Reservation
# Import database object
from app import db


@reservations.route('/reservation_list')
def reservation_list():
    reservations = Reservation.subordinates_editable(Reservation.query, current_user).all()
    reservations = list(filter(lambda r: r.last_status() != ReservationStatus.CANCELED, reservations))

    return render_template('reservations/list.html', reservations=reservations, submit_form=SubmitForm())


@reservations.route('/reservation_details')
def reservation_details():
    reservation_id = request.args.get('reservation_id')
    reservation = Reservation.query.filter_by(id=reservation_id).first()

    return reservation.serialize(payment=True, reservations_rooms=True, room=True, room_category=True)


@reservations.route('/dashboard')
def dashboard():
    user_form = UserForm()
    status_form = StatusForm()
    return render_template('reservations/dashboard.html', user_form=user_form, status_form=status_form)


@reservations.route('/email_autocomplete', methods=['GET'])
def email_autocomplete():
    users = User.query.all()
    emails = list(map(lambda u: u.email, users))

    return jsonify(json_emails=emails)


@reservations.route('/load_rooms', methods=['GET', 'POST'])
def load_rooms():
    selected_capacity = int(json.loads(request.data)['capacity'])
    selected_type = int(json.loads(request.data)['type'])

    hotels = []
    json_result = []
    if current_user.role == UserRole.ADMIN.value:
        hotels = Hotel.query.all()
    elif current_user.role == UserRole.DIRECTOR.value:
        hotels = Hotel.query.filter_by(owner=current_user).all()
    elif current_user.role == UserRole.RECEPTIONIST.value:
        hotels = Hotel.query.filter(Hotel.receptionists.any(id=current_user.id)).all()
    
    if not hotels:
        return jsonify(status=500, message='You are not assigned to any hotel.')

    for hotel in hotels:
        json_hotel = {
            'name': hotel.name,
            'expanded': True,
            'children': []
        }
        rooms = Room.query.join(RoomCategory).join(Hotel).filter(Hotel.id == hotel.id).all()
        rooms = filter_rooms(rooms, selected_capacity, selected_type)
        for room in rooms:
            json_room = {
                'id': room.id,
                'name': '#' + str(room.number) + \
                    ' (' + RoomType(room.room_category.type).name.lower() + ') - ' + \
                    str(room.beds) + ' bed' + ('s' if room.beds > 1 else ''),
                'status': 'Free' if is_room_free(room) else 'Busy'
            }
            json_hotel['children'].append(json_room)
        json_result.append(json_hotel)

    return jsonify(json_result)

@reservations.route('/get_reservations/<date:date_from>/<date:date_to>', methods=['GET'])
def load_reservations(date_from, date_to):
    # reservations = Reservation.subordinates_editable(ReservationRoom.filter(Reservation.query, '2020-01-01', '2020-12-31'), 2).all()
    # Reservation.query -> TO, co chci na vystup
    # Reservation.subordinates_editable -> K cemu potrebuju opravneni + join
    # ReservationRoom.filter -> podle ceho filtruju (Je potreba zavolat subordinates_editable pro join)
    json_arr = []
    reservations = Reservation.subordinates_editable(ReservationRoom.filter(Reservation.query, date_from, date_to), current_user).all()
    reservations = list(filter(lambda r: r.last_status() != ReservationStatus.CANCELED, reservations))

    for reservation in reservations:
        json_arr.append(reservation.serialize(True, True, True, True, True))
    return jsonify(json_arr)


@reservations.route('/create_reservation', methods=['GET', 'POST'])
def create_reservation():
    data = request.get_json()
    customer_id = data['customer_id']
    rooms_dates = data['reservations_rooms']

    customer = User.query.filter_by(id=customer_id).first()
    receptionist = None
    if current_user.is_authenticated and current_user is not customer:
        receptionist = current_user

    real_amount = 0
    reservations_rooms = []
    for room_date in rooms_dates:
        room = Room.query.filter_by(id=room_date['room_id']).first()
        date_from = datetime.strptime(room_date['date_from'], '%d-%m-%Y')
        date_to = datetime.strptime(room_date['date_to'], '%d-%m-%Y')

        real_amount += room.room_category.price * (date_to - date_from).days

        reservation_room = ReservationRoom(date_from, date_to)
        reservation_room.room = room
        reservations_rooms.append(reservation_room)

    tax = float(real_amount) * 0.21
    full_amount = float(real_amount) + tax
    block_amount = full_amount * 0.5

    payment = Payment(block_amount, full_amount, tax, False, False)
    reservation = Reservation(customer, payment)
    reservation.reservations_rooms.extend(reservations_rooms)
    history = History(reservation, ReservationStatus.NEW.value, datetime.now(), receptionist)

    db.session.add(reservation)
    db.session.add(history)
    db.session.commit()

    reserv_room_ids = []
    for rr in reservations_rooms:
        reserv_room_ids.append(rr.id)
    return jsonify(reserv_room_ids=reserv_room_ids, message='Reservation successfully created')


@reservations.route('/edit_reservation', methods=['GET', 'POST'])
def edit_reservation():
    data = request.get_json()
    reserv_room_id = data['reserv_room_id']
    status = int(data['status'])
    payment = int(data['payment'])
    date_from = datetime.strptime(data['date_from'], '%d-%m-%Y')
    date_to = datetime.strptime(data['date_to'], '%d-%m-%Y')

    reserv_room = ReservationRoom.query.filter_by(id=reserv_room_id).first()
    reserv_room.date_from = date_from
    reserv_room.date_to = date_to
    db.session.add(reserv_room)
    db.session.commit()

    reservation = Reservation.query.filter_by(id=reserv_room.reservation.id).first()
    if reservation:
        if status != reservation.last_status():
            history = History(reservation, status, datetime.now(), current_user)
            db.session.add(history)
        update_payment(reservation, payment)
        db.session.commit()

    return jsonify(message='Reservation successfully updated')


@reservations.route('/delete_reservation/<int:reservation_id>', methods=['GET', 'POST'])
def delete_reservation(reservation_id):
    form = SubmitForm(request.form)

    reservation = Reservation.query.filter_by(id=reservation_id).first()
    if not reservation:
        flash('Wrong reservation!', 'error')
        return redirect(url_for('reservations.reservation_list'))

    if form.validate_on_submit():
        history = History(reservation, ReservationStatus.CANCELED.value, datetime.now(), current_user)
        for reserv_room in reservation.reservations_rooms:
            reserv_room.is_active = False

        db.session.add(reservation)
        db.session.add(history)
        db.session.commit()
        flash('Reservation #{} was canceled.'.format(reservation.id), 'info')
    else:
        flash('Wrong form!', 'error')

    return redirect(url_for('reservations.reservation_list'))


@reservations.route('/delete_reserv_room', methods=['GET', 'POST'])
def delete_reserv_room():
    reserv_room_id = request.args.get('reserv_room_id')

    # inactivate selected reservation_room
    reservation_room = ReservationRoom.query.filter_by(id=reserv_room_id).first()
    reservation_room.is_active = False
    db.session.add(reservation_room)
    db.session.commit()

    # check other reservations_rooms of related reservation
    # if no one is active, cancel the whole reservation
    reservation = Reservation.query.filter_by(id=reservation_room.reservation.id).first()
    to_cancel = True
    for reserv_room in reservation.reservations_rooms:
        if reserv_room.is_active:
            to_cancel = False
    if to_cancel:
        history = History(reservation, ReservationStatus.CANCELED.value, datetime.now(), current_user)
        db.session.add_all([reservation, history])
        db.session.commit()

    return jsonify(message='Reservation successfully deleted')

def filter_rooms(rooms, selected_capacity, selected_type):
    if selected_capacity:
        if (selected_capacity >= 4):
            rooms = filter(lambda room: room.beds >= selected_capacity, rooms)
        elif (selected_capacity > 0):
            rooms = filter(lambda room: room.beds == selected_capacity, rooms)
    if selected_type:
        rooms = filter(lambda room: RoomType(room.room_category.type) == RoomType(selected_type), rooms)

    return rooms


def is_room_free(room, date=date.today()):
    is_free = True
    for res_room in room.reservations_rooms:
        if date >= res_room.date_from and date < res_room.date_to and res_room.is_active:
            is_free = False

    return is_free
    

def update_payment(reservation, payment):
    if payment == 0:
        reservation.payment.is_blocked = False
        reservation.payment.is_paid = False
    elif payment == 1:
        reservation.payment.is_blocked = True
        reservation.payment.is_paid = False
    elif payment == 2:
        reservation.payment.is_blocked = True
        reservation.payment.is_paid = True
