from flask import request, make_response
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required
from wtforms_components import read_only
from datetime import datetime, timedelta

from ..models import User, UserRole, HotelStars, Address, RoomCategory, Room, Hotel, RoomType

class ReservationForm(FlaskForm):
    category = QuerySelectField('Category',      \
        get_label = lambda t: "{}".format(t.type), \
        validators=[Required()])


    # RM {{
    beds_1 = QuerySelectField('Beds',      \
        get_pk          = lambda t: t.beds, \
        get_label = lambda t: "{}".format(t.beds))

    beds_2 = QuerySelectField('Beds',      \
        get_pk          = lambda t: t.id, \
        get_label       = lambda t: "{}".format(t.beds))

    beds_3 = QuerySelectField('Beds',      \
        get_pk          = lambda t: t.id, \
        get_label       = lambda t: "{}".format(t.beds))

    # }}
    date_from   = StringField('Date From')
    date_to     = StringField('Date To')
    
    email       = StringField('E-mail',      validators=[Required()])

    reserve     = SubmitField('Reserve')

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        if 'obj' in kwargs:
            self.obj = kwargs['obj']
        if 'date_from' in kwargs:
            self.df = kwargs['date_from']
        if 'date_to' in kwargs:
            self.dt = kwargs['date_to']
        if 'user' in kwargs:
            self.usr = kwargs['user']

        # HOTEL != RESERVATION => obj != hotel, hotel=kwargs['hotel']
        # REMOVE NAH
        self.category.query_factory = lambda: RoomCategory.query.filter_by(hotel_id=self.obj.id)
        q = RoomCategory.query.filter_by(hotel_id=self.obj.id, type='STANDARD').first()
        if q is not None:
            self.beds_1.query_factory = \
                lambda: Room.query.filter_by(room_category_id = RoomCategory.query.filter_by(hotel_id=self.obj.id, type='STANDARD').first().id)
        else:
            del self.beds_1

        q = RoomCategory.query.filter_by(hotel_id=self.obj.id, type='LUX').first()
        if q is not None:
            self.beds_2.query_factory = \
                lambda: Room.query.filter_by(room_category_id = RoomCategory.query.filter_by(hotel_id=self.obj.id, type='LUX').one().id)
        else:
            self.beds_2.data = None

        q = RoomCategory.query.filter_by(hotel_id=self.obj.id, type='BUSINESS').first()
        if q is not None:
            self.beds_3.query_factory = \
                lambda: Room.query.filter_by(room_category_id = RoomCategory.query.filter_by(hotel_id=self.obj.id, type='BUSINESS').one().id)
        else:
            del self.beds_3

        #  }} REMOVE

    def authorised(self):
        self.email.data = self.usr.email

    def unauthorised(self):
        self.category.query_factory = lambda: RoomCategory.query.filter_by(hotel_id=self.obj.id)
