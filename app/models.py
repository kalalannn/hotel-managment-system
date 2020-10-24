from sqlalchemy import create_engine, Column, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from sqlalchemy import Date, Text, String, Integer, Numeric, Boolean


# creates engine for provided database path
engine = create_engine('postgresql://postgres:postgres@localhost:5432/mydb')
# creates configured "Session" factory class
Session = sessionmaker(bind=engine)

Base = declarative_base()


''' User model '''
class User(Base):
    __tablename__  = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    birth_date = Column(Date)

    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    role = relationship('Role', back_populates='user', uselist=False)
    hotels = relationship('Hotel', back_populates='owner')
    reservs_cust = relationship('Reservation', foreign_keys='Reservation.customer_id', back_populates='customer')
    reservs_recept = relationship('Reservation', foreign_keys='Reservation.receptionist_id', back_populates='receptionist')
    feedbacks = relationship("Feedback", back_populates="user")

    def __init__(self, username, password, first_name, last_name, email, birth_date, role):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.birth_date = birth_date
        self.role = role

    def __repr__(self):
        return "<User(username='%s', first_name='%s', last_name='%s', role='%s')>" % (
            self.username, self.first_name, self.last_name, self.role)


''' Role model '''
class Role(Base):
    __tablename__  = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))

    user = relationship("User", back_populates="role")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role(name='%s')>" % (self.name)


''' Feedback model '''
class Feedback(Base):
    __tablename__  = 'feedbacks'

    id = Column(Integer, primary_key=True)
    text = Column(Text)
    rating = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    hotel_id = Column(Integer, ForeignKey('hotels.id'), nullable=False)

    user = relationship("User", back_populates="feedbacks")
    hotel = relationship("Hotel", back_populates="feedbacks")

    def __init__(self, text, rating, user, hotel):
        self.text = text
        self.rating = rating
        self.user = user
        self.hotel = hotel

    def __repr__(self):
        return "<Feedback(text='%s', rating='%s')>" % (self.text, self.rating)


''' Hotel model '''
class Hotel(Base):
    __tablename__  = 'hotels'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    stars = Column(Integer)
    address = Column(Text)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="hotels")
    feedbacks = relationship("Feedback", back_populates="hotel")
    room_categories = relationship('RoomCategory', back_populates='hotel')

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
class Status(Base):
    __tablename__  = 'statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))

    reservations = relationship("Reservation", back_populates="status")

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Status(name='%s')>" % (self.name)


''' Payment model '''
class Payment(Base):
    __tablename__  = 'payments'

    id = Column(Integer, primary_key=True)
    block_amount = Column(Numeric)
    full_amount = Column(Numeric)
    tax = Column(Numeric)
    is_blocked = Column(Boolean)
    is_payed = Column(Boolean)

    reservation = relationship("Reservation", back_populates="payment")

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
class ReservationRoom(Base):
    __tablename__  = 'reservations_rooms'

    id = Column(Integer, primary_key=True)
    date_from = Column(Date)
    date_to = Column(Date)

    reservation_id = Column(Integer, ForeignKey('reservations.id'))
    room_id = Column(Integer, ForeignKey('rooms.id'))

    reservation = relationship("Reservation", back_populates="rooms")
    room = relationship("Room", back_populates="reservations")

    def __init__(self, date_from, date_to):
        self.date_from = date_from
        self.date_to = date_to

    def __repr__(self):
        return "<ReservationRoom(date_from='%s', date_to='%s')>" % (self.date_from, self.date_to)


''' Reservation model '''
class Reservation(Base):
    __tablename__  = 'reservations'

    id = Column(Integer, primary_key=True)

    status_id = Column(Integer, ForeignKey('statuses.id'))
    customer_id = Column(Integer, ForeignKey('users.id'))
    receptionist_id = Column(Integer, ForeignKey('users.id'))
    payment_id = Column(Integer, ForeignKey('payments.id'))

    status = relationship('Status', back_populates='reservations')
    customer = relationship('User', foreign_keys=customer_id, back_populates='reservs_cust')
    receptionist = relationship('User', foreign_keys=receptionist_id, back_populates='reservs_recept')
    payment = relationship('Payment', back_populates="reservation", uselist=False)
    rooms = relationship('ReservationRoom', back_populates='reservation')

    def __init__(self, status, customer, receptionist, payment):
        self.status = status
        self.customer = customer
        self.receptionist = receptionist
        self.payment = payment
        
    def __repr__(self):
        return "<Reservation(id='%s')>" % (self.id)


''' Room-equipment association '''
rooms_equipments = Table('rooms_equipments', Base.metadata,
    Column('room_id', Integer, ForeignKey('rooms.id')),
    Column('equipment_id', Integer, ForeignKey('equipments.id'))
)


''' Room model '''
class Room(Base):
    __tablename__  = 'rooms'

    id = Column(Integer, primary_key=True)
    beds = Column(Integer)

    room_category_id = Column(Integer, ForeignKey('room_categories.id'))

    room_category = relationship('RoomCategory', back_populates='rooms')
    reservations = relationship('ReservationRoom', back_populates='room')
    equipments = relationship('Equipment', secondary=rooms_equipments, back_populates='rooms')

    def __init__(self, beds, room_category):
        self.beds = beds
        self.room_category = room_category

    def __repr__(self):
        return "<Room(id='%s', beds='%s')>" % (self.id, self.beds)


''' Room category model '''
class RoomCategory(Base):
    __tablename__  = 'room_categories'

    id = Column(Integer, primary_key=True)
    type = Column(String(32))
    price = Column(Numeric)

    hotel_id = Column(Integer, ForeignKey('hotels.id'))

    hotel = relationship('Hotel', back_populates='room_categories')
    rooms = relationship('Room', back_populates='room_category')

    def __init__(self, type, price, hotel):
        self.type = type
        self.price = price
        self.hotel = hotel

    def __repr__(self):
        return "<RoomCategory(type='%s', price='%s')>" % (self.type, self.price)


''' Equipment model '''
class Equipment(Base):
    __tablename__  = 'equipments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    rooms = relationship('Room', secondary=rooms_equipments, back_populates='equipments')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Equipment(name='%s')>" % (self.name)