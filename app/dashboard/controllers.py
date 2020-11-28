from flask import request, render_template, jsonify, json
from flask_login import current_user
from datetime import datetime, date
from decimal import Decimal
import uuid

import jsonpickle

from . import dashboard
# Import needed forms and models
from .forms import UserForm, StatusForm
from ..models import User, UserRole, Hotel, Room, RoomCategory, ReservationRoom, ReservationStatus, \
    RoomType, Payment, History, Reservation
# Import database object
from app import db


@dashboard.route('/show')
def show():
    user_form = UserForm()
    status_form = StatusForm()
    return render_template('dashboard/show.html', user_form=user_form, status_form=status_form)


@dashboard.route('/email_autocomplete', methods=['GET'])
def email_autocomplete():
    users = User.query.all()
    emails = list(map(lambda u: u.email, users))

    return jsonify(json_emails=emails)


@dashboard.route('/find_user', methods=['GET'])
def find_user():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()

    return jsonify(
        {'first_name': user.first_name,
        'last_name': user.last_name})


@dashboard.route('/load_rooms', methods=['GET', 'POST'])
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


@dashboard.route('/load_reservations', methods=['GET', 'POST'])
def load_reservations():
    res_rooms = ReservationRoom.query.all()
    res_rooms = list(filter(lambda rr: rr.is_active, res_rooms))

    json_result = []
    for res_room in res_rooms:
        json_reservation = {
                'start': str(res_room.date_from),
                'end': str(res_room.date_to),
                'id': res_room.id,
                'resource': res_room.room_id,
                'text': res_room.reservation.customer.last_name,
                'status': ReservationStatus(res_room.reservation.status).name,
                'payment': 'paid' if res_room.reservation.payment.is_paid else \
                    ('blocked' if res_room.reservation.payment.is_blocked else 'unpaid'),
                'room_number': res_room.room.number
            }
        json_result.append(json_reservation)
    return jsonify(json_result)


## TOhle sem rozhodne nepatri
@dashboard.route('/get_user', methods=['GET', 'POST'])
def get_user():
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


@dashboard.route('/create_reservation', methods=['GET', 'POST'])
def create_reservation():
    data = request.get_json()
    customer_id = data['customer_id']
    rooms_dates = data['reservations_rooms']

    customer = User.query.filter_by(id=customer_id).first()
    receptionist = None
    if current_user is not customer:
        receptionist = current_user

    full_amount = 0
    reservations_rooms = []
    for room_date in rooms_dates:
        room = Room.query.filter_by(id=room_date['room_id']).first()
        date_from = datetime.strptime(room_date['date_from'], '%d-%m-%Y')
        date_to = datetime.strptime(room_date['date_to'], '%d-%m-%Y')

        full_amount += room.room_category.price * (date_to - date_from).days

        reservation_room = ReservationRoom(date_from, date_to)
        reservation_room.room = room
        reservations_rooms.append(reservation_room)

    payment = Payment(float(full_amount) * 0.5, full_amount)
    reservation = Reservation(ReservationStatus.NEW.value, customer, payment)
    reservation.reservations_rooms.extend(reservations_rooms)
    history = History(reservation, ReservationStatus.NEW.value, datetime.now(), receptionist)

    db.session.add(reservation)
    db.session.add(history)
    db.session.commit()

    reserv_room_ids = []
    for rr in reservations_rooms:
        reserv_room_ids.append(rr.id)
    return jsonify(reserv_room_ids=reserv_room_ids, message='Reservation successfully created')


@dashboard.route('/edit_reservation', methods=['GET', 'POST'])
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
        reservation.status = ReservationStatus(status).value
        update_payment(reservation, payment)
        db.session.add(reservation)
        db.session.commit()

    return jsonify(message='Reservation successfully updated')


@dashboard.route('/delete_reservation', methods=['GET', 'POST'])
def delete_reservation():
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
        reservation.status = ReservationStatus.CANCELED.value
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
