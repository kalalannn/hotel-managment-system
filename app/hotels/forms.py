from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required
from wtforms_components import read_only
from wtforms.widgets import TextArea
from ..models import User, UserRole, HotelStars, Address, RoomCategory

class SearchForm(FlaskForm):
    name    = StringField('Name')
    stars   = SelectField('Stars')
    submit  = SubmitField('Search')

class AddRoomForm(FlaskForm):
    room_category = QuerySelectField('Category',      \
        get_label = lambda t: "{}".format(t.type), \
        validators=[Required()])

    number_of_beds  = StringField('Number of beds')
    numbers_from = StringField('Numbers from')
    numbers_to = StringField('Numbers to')
    addRoom         = SubmitField('Add Rooms')
    
    def __init__(self, *args, **kwargs):
        super(AddRoomForm, self).__init__(*args, **kwargs)
        self.obj = kwargs['obj']

    def __repr__(self):
        return 'room_category={}'.format(self.room_category)
    
    def add_room(self):
        self.room_category.query_factory = lambda: RoomCategory.query.filter_by(hotel_id=self.obj.id)


class HotelForm(FlaskForm):
    name       = StringField('Name',            \
        validators=[Required()])

    stars      = QuerySelectField('Stars',      \
        get_pk      = lambda s: s.value,        \
        get_label   = lambda s: '*' * s.value,  \
        validators  = [Required()])

    owner      = QuerySelectField('Owner',      \
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
        self.obj = kwargs['obj']

    def __repr__(self):
        return 'name={}, stars={}, desc={}'.format(self.name, self.stars, self.description)

    def admin(self):
        self.stars.query_factory = lambda: HotelStars
        self.stars.data = HotelStars(self.obj.stars)
        self.owner.query_factory = lambda: User.query.filter_by(role=UserRole.DIRECTOR.value).all()
        self.address_country.data = self.obj.address.country
        self.address_post_code.data = self.obj.address.post_code
        self.address_city.data = self.obj.address.city
        self.address_street.data = self.obj.address.street
        self.address_number.data = self.obj.address.number


    # self.obj is Necessary to limit choises
    def director(self):
        # self.stars.query_factory = lambda: [ HotelStars(self.obj.stars) ]
        # self.owner.query_factory = lambda: [ self.obj.owner ]
        del self.name
        del self.stars
        del self.owner
        del self.address_country  
        del self.address_post_code
        del self.address_city     
        del self.address_street   
        del self.address_number   
        # read_only(self.name)
        # read_only(self.stars)
        # read_only(self.owner)
