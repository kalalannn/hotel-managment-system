from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


''' User model '''
class User(UserMixin, db.Model):
    __tablename__  = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    birth_date = db.Column(db.Date)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', back_populates='user', uselist=False)
    hotels = db.relationship('Hotel', back_populates='owner')
    reservs_cust = db.relationship('Reservation', foreign_keys='Reservation.customer_id', back_populates='customer')
    reservs_recept = db.relationship('Reservation', foreign_keys='Reservation.receptionist_id', back_populates='receptionist')
    feedbacks = db.relationship("Feedback", back_populates="user")

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password, first_name, last_name, email, birth_date, role):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        self.role = role

    def __repr__(self):
        return "<User(username='%s', first_name='%s', last_name='%s', role='%s')>" % (
            self.username, self.first_name, self.last_name, self.role)

''' Role model '''
class Role(db.Model):
    __tablename__  = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    user = db.relationship("User", back_populates="role")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role(name='%s')>" % (self.name)

''' Feedback model '''
class Feedback(db.Model):
    __tablename__  = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    rating = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'), nullable=False)

    user = db.relationship("User", back_populates="feedbacks")
    hotel = db.relationship("Hotel", back_populates="feedbacks")

    def __init__(self, text, rating, user, hotel):
        self.text = text
        self.rating = rating
        self.user = user
        self.hotel = hotel

    def __repr__(self):
        return "<Feedback(text='%s', rating='%s')>" % (self.text, self.rating)

''' Hotel model '''
class Hotel(db.Model):
    __tablename__  = 'hotels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    stars = db.Column(db.Integer)
    address = db.Column(db.Text)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship("User", back_populates="hotels")
    feedbacks = db.relationship("Feedback", back_populates="hotel")
    room_categories = db.relationship('RoomCategory', back_populates='hotel')

    def __init__(self, name, description, stars, address, owner):
        self.name = name 
        self.description = description 
        self.owner = owner
        self.stars = stars
        self.address = address
        self.owner = owner

    def __repr__(self):
        return "<Hotel(name='%s', stars='%s')>" % (self.name, self.stars)

''' Status model '''
class Status(db.Model):
    __tablename__  = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    reservations = db.relationship("Reservation", back_populates="status")

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Status(name='%s')>" % (self.name)

''' Payment model '''
class Payment(db.Model):
    __tablename__  = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    block_amount = db.Column(db.Numeric)
    full_amount = db.Column(db.Numeric)
    tax = db.Column(db.Numeric)
    is_blocked = db.Column(db.Boolean)
    is_payed = db.Column(db.Boolean)

    reservation = db.relationship("Reservation", back_populates="payment")

    def __init__(self, block_amount, full_amount, tax, is_blocked=False, is_payed=False):
        self.block_amount = block_amount
        self.full_amount = full_amount
        self.tax = tax
        self.is_blocked = is_blocked
        self.is_payed = is_payed

    def __repr__(self):
        return "<Payment(block_amount='%s', full_amount='%s', is_blocked='%s', is_payed='%s')>" % (
            self.block_amount, self.full_amount, self.is_blocked, self.is_payed)

''' Reservation-room model '''
class ReservationRoom(db.Model):
    __tablename__  = 'reservations_rooms'

    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.Date)
    date_to = db.Column(db.Date)

    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))

    reservation = db.relationship("Reservation", back_populates="rooms")
    room = db.relationship("Room", back_populates="reservations")

    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to

    def __repr__(self):
        return "<ReservationRoom(date_from='%s', date_to='%s')>" % (self.date_from, self.date_to)


''' Reservation model '''
class Reservation(db.Model):
    __tablename__  = 'reservations'

    id = db.Column(db.Integer, primary_key=True)

    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    receptionist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))

    status = db.relationship('Status', back_populates='reservations')
    customer = db.relationship('User', foreign_keys=customer_id, back_populates='reservs_cust')
    receptionist = db.relationship('User', foreign_keys=receptionist_id, back_populates='reservs_recept')
    payment = db.relationship('Payment', back_populates="reservation", uselist=False)
    rooms = db.relationship('ReservationRoom', back_populates='reservation')

    def __init__(self, status, customer, receptionist, payment):
        self.status = status
        self.customer = customer
        self.receptionist = receptionist
        self.payment = payment
        
    def __repr__(self):
        return "<Reservation(id='%s')>" % (self.id)


''' Room-equipment association '''
rooms_equipments = db.Table('rooms_equipments', db.metadata,
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id')),
    db.Column('equipment_id', db.Integer, db.ForeignKey('equipments.id'))
)


''' Room model '''
class Room(db.Model):
    __tablename__  = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    beds = db.Column(db.Integer)

    room_category_id = db.Column(db.Integer, db.ForeignKey('room_categories.id'))

    room_category = db.relationship('RoomCategory', back_populates='rooms')
    reservations = db.relationship('ReservationRoom', back_populates='room')
    equipments = db.relationship('Equipment', secondary=rooms_equipments, back_populates='rooms')

    def __init__(self, beds, room_category):
        self.beds = beds
        self.room_category = room_category

    def __repr__(self):
        return "<Room(id='%s', beds='%s')>" % (self.id, self.beds)


''' Room category model '''
class RoomCategory(db.Model):
    __tablename__  = 'room_categories'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))
    price = db.Column(db.Numeric)

    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))

    hotel = db.relationship('Hotel', back_populates='room_categories')
    rooms = db.relationship('Room', back_populates='room_category')

    def __init__(self, type, price, hotel):
        self.type = type
        self.price = price
        self.hotel = hotel

    def __repr__(self):
        return "<RoomCategory(type='%s', price='%s')>" % (self.type, self.price)


''' Equipment model '''
class Equipment(db.Model):
    __tablename__  = 'equipments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    rooms = db.relationship('Room', secondary=rooms_equipments, back_populates='equipments')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Equipment(name='%s')>" % (self.name)