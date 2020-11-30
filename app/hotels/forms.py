from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required
from wtforms_components import read_only
from wtforms.widgets import TextArea

from datetime import datetime, timedelta

from ..models import User, UserRole, HotelStars, Address
from ..models import RoomCategory, RoomType


class SearchForm(FlaskForm):
    name    = StringField('Search')

    # stars   = QuerySelectField('Stars',         \
    #     query_factory   = lambda : HotelStars,  \
    #     get_pk          = lambda s: s.value,    \
    #     get_label       = lambda s: '*' * s.value,    \
    #     allow_blank     = True)

    country = QuerySelectField('Country',       \
        query_factory   = lambda: Address.query.distinct(Address.country).all(), \
        get_pk          = lambda a: a.id,       \
        get_label       = lambda a: a.country,  \
        allow_blank     = True)

    city    = QuerySelectField('City',          \
        query_factory   = lambda: Address.query.distinct(Address.city).all(),   \
        get_pk          = lambda a: a.id,       \
        get_label       = lambda a: "{} {}".format(a.post_code, a.city),        \
        allow_blank     = True)

    date_from           = DateField('From', \
        default = datetime.today, format='%d-%m-%Y')
    date_to             = DateField('To',   \
        default = datetime.today() + timedelta(days=1), format='%d-%m-%Y')

    people_count        = StringField('Persons',   default=2)
    # rooms_count         = StringField('Rooms',    default=1)

    submit  = SubmitField('Search')

class HotelForm(FlaskForm):
    name       = StringField('Name',            \
        validators=[Required()])

    stars      = QuerySelectField('Stars',      \
        query_factory = lambda: HotelStars,     \
        get_pk      = lambda s: s.value,        \
        get_label   = lambda s: '*' * s.value,  \
        validators  = [Required()])

    owner      = QuerySelectField('Owner',      \
        query_factory = lambda: User.query.filter_by(role=UserRole.DIRECTOR.value).all(), \
        get_label = lambda u: "{} {}".format(u.first_name, u.last_name), \
        validators=[Required()])

    address_country    = StringField('Country',    validators=[Required()])
    address_post_code  = StringField('Post code',  validators=[Required()])
    address_city       = StringField('City',       validators=[Required()])
    address_street     = StringField('Street',     validators=[Required()])
    address_number     = StringField('Number',     validators=[Required()])

    description = StringField('Description',     \
        widget=TextArea(),
        validators=[Required()])
    

    submit     = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(HotelForm, self).__init__(*args, **kwargs)
        if 'obj' in kwargs:
            self.obj = kwargs['obj']

    def __repr__(self):
        return 'name={}, stars={}, desc={}'.format(self.name, self.stars, self.description)

    def admin(self):
        self.stars.query_factory = lambda: HotelStars
        self.owner.query_factory = lambda: User.query.filter_by(role=UserRole.DIRECTOR.value).all()
        if hasattr(self, 'obj'):
            self.stars.data = HotelStars(self.obj.stars)
            self.address_country.data = self.obj.address.country
            self.address_post_code.data = self.obj.address.post_code
            self.address_city.data = self.obj.address.city
            self.address_street.data = self.obj.address.street
            self.address_number.data = self.obj.address.number

    def director(self):
        del self.name
        del self.stars
        del self.owner
        del self.address_country  
        del self.address_post_code
        del self.address_city     
        del self.address_street   
        del self.address_number   

class RoomCategoryForm(FlaskForm):
    type = QuerySelectField('Type',      \
        query_factory   = lambda: RoomType, \
        get_pk          = lambda t: t.value, \
        get_label       = lambda t: RoomType(t.value).name, \
        validators=[Required()])

    price = IntegerField('Price CZK',
        validators=[Required()])
    description = StringField('Description',     \
        widget=TextArea(),
        validators=[Required()])

    submit        = SubmitField('Save')

class RoomForm(FlaskForm):
    room_category = QuerySelectField('Category',      \
        get_pk          = lambda c: c.id,   \
        get_label       = lambda c: "{} ({},- CZK)".format(RoomType(c.type).name, c.price), \
        validators = [Required()])

    number = IntegerField('Room #',
        validators=[Required()])

    beds            = IntegerField('Beds',
        validators=[Required()])

    submit         = SubmitField('Save')
    
    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        if 'obj' in kwargs:
            self.room_category.query_factory = \
                lambda: RoomCategory.query.filter_by(hotel_id=kwargs['obj'].room_category.hotel_id) #.distinct("type")

        if 'hotel_id' in kwargs:
            self.room_category.query_factory = \
                lambda: RoomCategory.query.filter_by(hotel_id=kwargs['hotel_id']) #.distinct("type")
