from flask import request, render_template, jsonify, json
from flask_login import current_user
from datetime import datetime, date
import uuid

from . import dashboard
# Import needed forms and models
from .forms import UserForm
from ..models import UserRole, Hotel, Room, RoomCategory, ReservationRoom, ReservationStatus, RoomType
# Import database object
from app import db


@dashboard.route('/show')
def show():
    form = UserForm()
    return render_template('dashboard/show.html', form=form)


LIST=["abc","abcd","abcde","abcdef","abcdef","abcdef","abcdef","abcdef","abcdef","abcdef","abcde","abcde","abcde","abcde"]

@dashboard.route('/autocomplete',methods=['GET'])
def autocomplete():
    search = request.args.get('term')
    return jsonify(json_list=LIST) 


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
                    ' (' + RoomType(room.room_category.type).name.lower() + ')',
                'capacity': room.beds,
                'status': 'Free' if is_room_free(room) else 'Busy'
            }
            json_hotel['children'].append(json_room)
        json_result.append(json_hotel)

    return jsonify(json_result)


@dashboard.route('/load_reservations', methods=['GET', 'POST'])
def load_reservations():
    month_start = datetime.fromisoformat(json.loads(request.data)['start'])
    month_end = datetime.fromisoformat(json.loads(request.data)['end'])

    res_rooms = ReservationRoom.query.filter(ReservationRoom.date_from >= month_start, ReservationRoom.date_to < month_end).all()

    json_result = []
    for res_room in res_rooms:
        json_reservation = {
                'start': str(res_room.date_from),
                'end': str(res_room.date_to),
                'id': uuid.uuid4(),
                'resource': res_room.room_id,
                'text': res_room.reservation.customer.last_name,
                'status': ReservationStatus(res_room.reservation.status).name,
                'isPaid': res_room.reservation.payment.is_payed,
            }
        json_result.append(json_reservation)

    return jsonify(json_result)


@dashboard.route('/create_reservation', methods=['GET', 'POST'])
def create_reservation():
    start_date = datetime.fromisoformat(json.loads(request.data)['start'])
    end_date = datetime.fromisoformat(json.loads(request.data)['end'])
    room_id = int(json.loads(request.data)['room'])
    first_name = json.loads(request.data)['first_name']
    last_name = json.loads(request.data)['last_name']

    # print(start_date)
    # print(end_date)
    # print(room_id)
    # print(first_name)
    # print(last_name)

    return jsonify({'t':'ttt'})


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
        if date >= res_room.date_from and date < res_room.date_to:
            is_free = False

    return is_free