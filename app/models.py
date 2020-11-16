from app import db
from sqlalchemy import CheckConstraint, column
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.helpers import Helper
from . import login_manager
from enum import Enum

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class UserRole(Enum):
    ANON = 1
    CUSTOMER = 2
    RECEPTIONIST = 3
    DIRECTOR = 4
    ADMIN = 5

class HotelStars(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

class RoomType(Enum):
    STANDARD = 1
    LUX = 2
    BUSINESS = 3

class ReservationStatus(Enum):
    CREATED = 1
    BOOKED = 2
    CANCELED = 3

class User(UserMixin, db.Model):
    __tablename__  = 'users'

    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.Text)
    last_name       = db.Column(db.Text)
    email           = db.Column(db.Text)
    password_hash   = db.Column(db.Text)
    is_active       = db.Column(db.Boolean)
    role            = db.Column(db.Integer, \
        CheckConstraint('role in (%s)' % (', '.join(str(r.value) for r in UserRole))))

    recept_hotel_id  = db.Column(db.Integer, \
        db.ForeignKey('hotels.id'))
    recept_hotels   = db.relationship('Hotel', \
        foreign_keys = recept_hotel_id, \
        back_populates = 'receptionists')

    own_hotels       = db.relationship('Hotel', \
        foreign_keys = 'Hotel.owner_id', \
        back_populates = 'owner',
        post_update = True)

    customer_reservations = db.relationship('Reservation', \
        foreign_keys = 'Reservation.customer_id', \
        back_populates = 'customer')

    receptionist_reservations = db.relationship('Reservation', \
        foreign_keys = 'Reservation.receptionist_id', \
        back_populates = 'receptionist')

    feedbacks       = db.relationship("Feedback", \
        back_populates="user")

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, _first_name, _last_name, _email, _password, _role, _is_active=True):
        self.first_name     = _first_name
        self.last_name      = _last_name
        self.email          = _email
        self.password_hash  = generate_password_hash(_password)
        self.role           = _role
        self.is_active      = _is_active

    def __repr__(self):
        return "<User(id='%s', email='%s', first_name='%s', last_name='%s', role='%s')>" % (
            self.id, self.email, self.first_name, self.last_name, self.role)

    # @staticmethod
    # def has_role(user, role_name):
    #     if not user.is_authenticated:
    #         return False
    #     return user.role.rate >= Role.query.filter_by(name=role_name).one().rate

class Hotel(db.Model):
    __tablename__  = 'hotels'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.Text)
    description     = db.Column(db.Text)
    stars           = db.Column(db.Integer, \
        CheckConstraint('stars in (%s)' % (', '.join(str(s.value) for s in HotelStars))))

    address         = db.relationship('Address', \
        back_populates='hotel', \
        uselist=False)

    owner_id        = db.Column(db.Integer, \
        db.ForeignKey('users.id', name='fk_hotel_owner_id'))
    owner           = db.relationship("User", \
        foreign_keys = owner_id, \
        back_populates = "own_hotels", \
        post_update = True)

    receptionists = db.relationship('User', \
        foreign_keys = 'User.recept_hotel_id', \
        back_populates = 'recept_hotels')

    room_categories = db.relationship('RoomCategory', \
        back_populates='hotel')

    feedbacks       = db.relationship("Feedback", \
        back_populates="hotel")

    def __init__(self, _name, _description, _stars, _address, _owner):
        super(Hotel, self).__init__()
        self.name           = _name
        self.description    = _description
        self.owner          = _owner
        self.stars          = _stars
        self.address        = _address
        self.owner          = _owner

    def __repr__(self):
        return "<Hotel(name={}, stars={}, description={})>".format(
            self.name, self.stars, self.description
        )

class Address(db.Model):
    __tablename__  = 'addresses'

    id          = db.Column(db.Integer, primary_key=True)
    country     = db.Column(db.Text)
    city        = db.Column(db.Text)
    post_code   = db.Column(db.Text)
    street      = db.Column(db.Text)
    number      = db.Column(db.Text)

    hotel_id    = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=True)
    hotel       = db.relationship("Hotel", \
        back_populates="address")
    
    # TODO user_id + user_address
    
    def __init__(self, _country, _city, _post_code, _street, _number, _hotel=None):
        self.country    = _country
        self.city       = _city
        self.post_code  = _post_code
        self.street     = _street
        self.number     = _number
        self.hotel      = _hotel
    
    def __repr__(self):
        return "<Address(country='%s', city='%s', post_code='%s', street='%s', number='%s')>" \
            % (self.country, self.city, self.post_code, self.street, self.number)

    def text(self):
        return '{} {}, {} {}, {}'.format(self.street, self.number, self.post_code, self.city, self.country)

class Feedback(db.Model):
    __tablename__  = 'feedbacks'

    id          = db.Column(db.Integer, primary_key=True)
    text        = db.Column(db.Text)
    stars       = db.Column(db.Integer, \
        CheckConstraint('stars in (%s)' % (', '.join(str(s.value) for s in HotelStars))))

    user_id     = db.Column(db.Integer, \
        db.ForeignKey('users.id'), nullable=False)
    user        = db.relationship("User", \
        back_populates="feedbacks")

    hotel_id    = db.Column(db.Integer, \
        db.ForeignKey('hotels.id'), nullable=False)
    hotel       = db.relationship("Hotel", \
        back_populates="feedbacks")

    def __init__(self, _text, _stars, _user, _hotel):
        self.text   = _text
        self.stars  = _stars
        self.user   = _user
        self.hotel  = _hotel

    def __repr__(self):
        return "<Feedback(text='%s', rating='%s')>" \
            % (self.text, self.rating)

class RoomCategory(db.Model):
    __tablename__  = 'room_categories'

    id          = db.Column(db.Integer, primary_key=True)
    price       = db.Column(db.Numeric)
    type        = db.Column(db.Text, \
        CheckConstraint("type in ('%s')" % ("', '".join([t.name for t in RoomType]))))

    hotel_id    = db.Column(db.Integer, \
        db.ForeignKey('hotels.id'))
    hotel       = db.relationship('Hotel', \
        back_populates='room_categories')

    rooms       = db.relationship('Room', \
        back_populates='room_category')

    def __init__(self, _type, _price, _hotel):
        self.type  = _type
        self.price = _price
        self.hotel = _hotel

    def __repr__(self):
        return "<RoomCategory(type='%s', price='%s')>" \
            % (self.type, self.price)

class Room(db.Model):
    __tablename__  = 'rooms'

    id              = db.Column(db.Integer, primary_key=True)
    number          = db.Column(db.Integer)
    beds            = db.Column(db.Integer)

    room_category_id= db.Column(db.Integer, \
        db.ForeignKey('room_categories.id'))
    room_category   = db.relationship('RoomCategory', \
        back_populates='rooms')

    reservations_rooms    = db.relationship('ReservationRoom', \
        back_populates='room')

    def __init__(self, _number, _beds, _room_category):
        self.number         = _number
        self.beds           = _beds
        self.room_category  = _room_category

    def __repr__(self):
        return "<Room(id={}, number={}, beds={}, room_category={}, price={})>".format(
            self.id, self.number, self.beds, \
            self.room_category.type, self.room_category.price
            )

class ReservationRoom(db.Model):
    __tablename__  = 'reservations_rooms'

    id              = db.Column(db.Integer, primary_key=True)
    date_from       = db.Column(db.Date)
    date_to         = db.Column(db.Date)

    room_id         = db.Column(db.Integer, \
        db.ForeignKey('rooms.id'))
    room            = db.relationship("Room", \
        back_populates="reservations_rooms")

    reservation_id  = db.Column(db.Integer, \
        db.ForeignKey('reservations.id'))
    reservation     = db.relationship("Reservation", \
        back_populates="reservations_rooms")


    def __init__(self, _date_from, _date_to):
        self.date_from  = _date_from
        self.date_to    = _date_to

    def __repr__(self):
        return "<ReservationRoom(date_from='%s', date_to='%s')>" \
            % (self.date_from, self.date_to)

class Reservation(db.Model):
    __tablename__  = 'reservations'

    id              = db.Column(db.Integer, primary_key=True)
    status          = db.Column(db.Text, \
        CheckConstraint("status in ('%s')" % ("', '".join([s.name for s in ReservationStatus]))))

    reservations_rooms = db.relationship('ReservationRoom', \
        back_populates='reservation')

    payment_id      = db.Column(db.Integer, db.ForeignKey('payments.id'))
    payment         = db.relationship('Payment', \
        back_populates="reservation", \
        uselist=False)

    customer_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    customer        = db.relationship('User', \
        foreign_keys = customer_id, \
        back_populates = 'customer_reservations')

    receptionist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receptionist    = db.relationship('User', \
        foreign_keys = receptionist_id, \
        back_populates = 'receptionist_reservations')


    def __init__(self, _status, _customer, _receptionist, _payment):
        self.status         = _status
        self.customer       = _customer
        self.receptionist   = _receptionist
        self.payment        = _payment

    def __repr__(self):
        return "<Reservation(id='%s', status='%s')>" \
            % (self.id, self.status)

class Payment(db.Model):
    __tablename__  = 'payments'

    id              = db.Column(db.Integer, primary_key=True)
    block_amount    = db.Column(db.Numeric)
    full_amount     = db.Column(db.Numeric)
    tax             = db.Column(db.Numeric)
    is_blocked      = db.Column(db.Boolean)
    is_payed        = db.Column(db.Boolean)

    reservation     = db.relationship("Reservation", \
        back_populates="payment")

    def __init__(self, _block_amount, _full_amount, _tax, _is_blocked=False, _is_payed=False):
        self.block_amount   = _block_amount
        self.full_amount    = _full_amount
        self.tax            = _tax
        self.is_blocked     = _is_blocked
        self.is_payed       = _is_payed

    def __repr__(self):
        return "<Payment(block_amount='%s', full_amount='%s', is_blocked='%s', is_payed='%s')>" \
            % (self.block_amount, self.full_amount, self.is_blocked, self.is_payed)
