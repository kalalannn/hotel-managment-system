from flask import request, session, render_template

from . import reservations
from ..models import Reservation, ReservationRoom, Room
from app import db

@reservations.route('/list/', methods=['GET', 'POST'])
def list():
    reservations = Reservation.query.order_by(Reservation.id)
    return render_template('reservations/list.html', reservations=reservations)

@reservations.route('/new/', methods=['GET', 'POST'])
def new():
    return render_template('reservations/new.html')

@reservations.route('/edit/', methods=['GET', 'POST'])
def edit():
    return render_template('reservations/edit.html')

@reservations.route('/show/', methods=['GET', 'POST'])
def show():
    return render_template('reservations/show.html')

@reservations.route('/delete/', methods=['GET', 'POST'])
def delete():
    return render_template('reservations/delete.html')
