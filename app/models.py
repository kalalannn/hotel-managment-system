from app import db
from sqlalchemy import CheckConstraint, column
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from enum import Enum
import string
import random

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
    LUX = 1
    BUSINESS = 2
    STANDARD = 3

class ReservationStatus(Enum):
    NEW = 1
    CANCELED = 2
    CHECKED_IN = 3
    CHECKED_OUT = 4

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
        # foreign_keys = 'Reservation.customer_id', \
        back_populates = 'customer')

    # receptionist_reservations = db.relationship('Reservation', \
    #     foreign_keys = 'Reservation.receptionist_id', \
    #     back_populates = 'receptionist')

    feedbacks       = db.relationship("Feedback", \
        back_populates="user")

    histories       = db.relationship("History", \
        back_populates="receptionist")

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_password():
        chars = string.ascii_uppercase + string.ascii_lowercase
        return ''.join(random.choice(chars) for _ in range(12))

    def __init__(self, _first_name, _last_name, _email,
                _password=generate_password.__func__(), _role=UserRole.ANON.value,
                _is_active=True, _recept_hotels=None):
        self.first_name     = _first_name
        self.last_name      = _last_name
        self.email          = _email
        self.password_hash  = generate_password_hash(_password)
        self.role           = _role
        self.is_active      = _is_active
        self.recept_hotels= _recept_hotels

    def __repr__(self):
        return "<User(id='%s', email='%s', first_name='%s', last_name='%s', role='%s', recept_hotel_id='%s')>" % (
            self.id, self.email, self.first_name, self.last_name, self.role, self.recept_hotel_id)

    @staticmethod # -> User
    def new(_first_name, _last_name, _email,
                _password=generate_password.__func__(), _role=UserRole.ANON.value,
                _is_active=True, _recept_hotels=None):
        user = User(_first_name, _last_name, _email,
            generate_password_hash(_password), _role,
            _is_active, _recept_hotels)
        db.session.add(user)
        return user

    @staticmethod # -> query
    def filter(query, first_name=None, last_name=None, email=None, role=None, is_active=True):
        if first_name:
            query = query.filter(User.first_name.ilike("%{}%".format(first_name)))
        if last_name:
            query = query.filter(User.last_name.ilike("%{}%".format(last_name)))
        if email:
            query = query.filter(User.email.ilike("%{}%".format(email)))
        if role and role != 0:
            query = query.filter(User.role == role)
        query = query.filter(User.is_active == is_active)
        return query

    @staticmethod # -> query
    def by_ids(query, user_ids):
        return query.filter(User.id.in_(user_ids))

    # Which Users can <get> and <edit> current_user
    @staticmethod # -> query
    def subordinates_editable(query, current_user):
        if current_user.is_authenticated:
            if current_user.role == UserRole.ADMIN.value:
                pass # ALL
            elif current_user.role == UserRole.DIRECTOR.value:
                query = query.join(Hotel, User.recept_hotels)
                query = Hotel.by_ids(query, [h.id for h in current_user.own_hotels])
            else:
                # RECEPTIONIST, CUSTOMER, ANON
                query = query.filter(User.id == current_user.id) # ONLY self
        else:
            # AnonMixin
            query = query.filter(False) # Neither
        return query

    # Which Users can <get>, but can NOT <edit> current_use
    @staticmethod # -> query
    def subordinates_not_editable(query, current_user):
        if current_user.is_authenticated:
            # ADMIN can <see> and <edit> ALL Users
            if current_user.role in [UserRole.DIRECTOR.value, UserRole.RECEPTIONIST.value]:
                # TODO CUSTOMERs + ANONs, that have done reservations
                pass
            else:
                # ADMIN, CUSTOMER, ANON
                query = query.filter(False) # Neither
        else:
            # AnonMixin
            query = query.filter(False) # Neither
        return query

    # Which attributes can INSERT OR UPDATE current_user
    # Which attribute values can be setten by current_user
    # user -> OLD User or None !!!! Must be subordinates_editable
    # other -> NEW values
    # first_name, last_name, email for now are without value rules
    @staticmethod # -> Bool
    def can_write(current_user, user, first_name, last_name, email, role, is_active, recept_hotel_id):
        _, _, _ = first_name, last_name, email
        if not user:
            # New user MUST be active
            if not is_active:
                return False

        # IF RECEPTIONIST then recept_hotel_id
        temp = bool(role == UserRole.RECEPTIONIST.value) + bool(recept_hotel_id is not None)
        if temp != 0 and temp != 2:
            return False, 'IF RECEPTIONIST then recept_hotel_id'


        if current_user.is_authenticated:
            if user: # Edit
                if current_user == user: # self
                    # Nobody can not activate or deactivate self
                    if user.is_active != is_active:
                        return False, 'Nobody can not activate or deactivate self'

                    # Nobody Can not edit self.recept_hotel_id
                    if user.recept_hotel_id != recept_hotel_id:
                        return False, 'Nobody Can not edit self.recept_hotel_id'

                    # Only ANON can edit self role to CUSTOMER
                    if current_user.role != UserRole.ANON.value:
                        if user.role != role and role != UserRole.CUSTOMER.value:
                            return False, 'Only ANON can edit self role'

                else: # ONLY for his subordinates_editable !!!
                    # Nobody can not edit password of another
                    # PASSWORD is not readable
                    # if user.password != password:
                    #     return False

                    # Only ADMIN can edit role
                    if current_user.role != UserRole.ADMIN.value:
                        if user.role != role:
                            return False, 'Only ADMIN can edit role'

                    # Only ADMIN or DIRECTOR can activate or deactviate
                    # Only ADMIN or DIRECTOR can edit recept_hotel_id 
                    if current_user.role < UserRole.DIRECTOR.value:
                        if user.is_active != is_active:
                            return False, 'Only ADMIN or DIRECTOR can activate or deactviate'
                        if user.recept_hotel_id != recept_hotel_id:
                            return False, 'Only ADMIN or DIRECTOR can edit recept_hotel_id'

            else: # New
                # ADMIN can create ALL Roles
                if current_user.role == UserRole.ADMIN.value:
                    pass
                # DIRECTOR can create RECEPTIOISTs + ANONs
                elif current_user.role >= UserRole.DIRECTOR.value:
                    if role not in [UserRole.RECEPTIONIST.value, UserRole.ANON.value]:
                        return False, 'DIRECTOR can create RECEPTIOISTs + ANONs'
                # RECEPTIONIST can create ONLY ANONs
                elif current_user.role == UserRole.RECEPTIONIST.value:
                    if role != UserRole.ANON.value:
                        return False, 'RECEPTIONIST can create ONLY ANONs'
                # ANON OR CUSTOMER can not create users
                else:
                    return False, 'ANON OR CUSTOMER can not create users'

                # Only DIRECTOR+ can create RECEPTIONISTS
                if current_user.role < UserRole.DIRECTOR.value and recept_hotel_id:
                    return False, 'Only DIRECTOR+ can create RECEPTIONISTS'
        else: # AnonMixin
            if user: # Edit
                # AnonMixin can not edit any User
                return False, 'AnonMixin can not edit any User'
            else: # New
                # AnonMixin can create CUSTOMER or ANON
                if role not in [UserRole.CUSTOMER.value, UserRole.ANON.value]:
                    return False, 'AnonMixin can create CUSTOMER or ANON'

                # AnonMixin can not set recept_hotel_is
                if recept_hotel_id:
                    return False, 'AnonMixin can not set recept_hotel_is'
        return True,''

    def serialize(self, recept_hotels=False, own_hotels=False, customer_reservations=False, feedbacks=False, histories=False):
        hash = {
            'id': self.id, 
            'first_name': self.first_name, 
            'last_name': self.last_name,
            'email': self.email,
            'role': {self.role: UserRole(self.role).name},
            'is_active': self.is_active,
            'recept_hotel_id': self.recept_hotel_id
        }
        if recept_hotels:
            hash['recept_hotels'] = self.recept_hotels.serialize()
            # hash['recept_hotels'] = []
            # for recept_hotel in self.recept_hotels:
            #     hash['recept_hotels'].append(recept_hotel.serialize())
        if own_hotels:
            hash['own_hotels'] = []
            for own_hotel in self.own_hotels:
                hash['own_hotels'].appen(own_hotel.serialize())
        if customer_reservations:
            hash['customer_reservations'] = []
            for customer_reservation in self.customer_reservations:
                hash['customer_reservations'].append(customer_reservation.serialize())
        # TODO feedbacks
        if histories:
            hash['histories'] = []
            for history in self.histories:
                hash['histories'].append(history.serialize())
        return hash

class Hotel(db.Model):
    __tablename__  = 'hotels'

    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.Text)
    description     = db.Column(db.Text)
    stars           = db.Column(db.Integer, \
        CheckConstraint('stars in (%s)' % (', '.join(str(s.value) for s in HotelStars))))
    is_active       = db.Column(db.Boolean)

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

    def __init__(self, _name, _description, _stars, _address, _owner, _is_active=True):
        super(Hotel, self).__init__()
        self.name           = _name
        self.description    = _description
        self.stars          = _stars
        self.address        = _address
        self.owner          = _owner

    def __repr__(self):
        return "<Hotel(name={}, stars={}, description={})>".format(
            self.name, self.stars, self.description
        )

    @staticmethod # -> query
    def except_ids(query, *hotel_ids):
        return query.filter(Hotel.id.notin_(hotel_ids))

    @staticmethod # -> query
    def by_ids(query, hotel_ids):
        return query.filter(Hotel.id.in_(hotel_ids))
    
    @staticmethod
    def filter(query, name=None, description=None, owner_id=None, stars=None, address_id=None, is_active=True):
        if name:
            query = query.filter(Hotel.name.ilike("%{}%".format(name)))
        if description:
            query = query.filter(Hotel.description.ilike("%{}%".format(description)))
        if owner_id:
            query = query.filter(Hotel.owner_id == owner_id)
        if stars:
            query = query.filter(Hotel.stars == stars)
        if address_id:
            query = query.filter(Hotel.address_id == address_id)
        # query = query.filter(Hotel.is_active == is_active)
        return query
    
    # Which Hotels can <get> and <edit> current_user
    @staticmethod
    def subordinates_editable(query, current_user):
        if current_user.is_authenticated:
            if current_user.role == UserRole.ADMIN.value:
                pass
            elif current_user.role == UserRole.DIRECTOR.value:
                query = Hotel.by_ids(query, [h.id for h in current_user.own_hotels])
            else:
                # RECEPTIONIST, CUSTOMER, ANON
                query = query.filter(False) # Neither
        else:
            # AnonMixin
            query = query.filter(False) # Neither
        return query

    # Which Hotels can <get>, but can NOT <edit> current_user
    @staticmethod # -> query
    def subordinates_not_editable(query, current_user):
        if current_user.is_authenticated:
            if current_user.role == UserRole.ADMIN.value:
                # ADMIN can edit ALL Hotels
                query = query.filter(False)
            elif current_user.role == UserRole.DIRECTOR.value:
                # DIRECTOR can edit ONLY his Hotels
                # that mean except DIRECTOR editable Hotels
                query = Hotel.except_ids(query, [h.id for h in current_user.own_hotels])
            else:
                # ALL can see ALL hotels
                pass
        return query

    def serialize(self, address=False, owner=False, receptionists=False, room_categories=False, feedbacks=False):
        hash = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'stars': {self.stars: HotelStars(self.stars).name},
            'is_active': self.is_active,
            'owner_id': self.owner_id,
        }
        if address:
            hash['address'] = self.address.serialize()
        if owner:
            hash['owner'] = self.owner.serialize()
        if receptionists:
            hash['receptionists'] = []
            for receptionist in self.receptionists:
                hash['receptionists'].append(receptionist.serialize())
        if room_categories:
            hash['room_categories'] = []
            for room_category in self.room_categories:
                hash['room_categories'].append(room_category.serialize())
        # TODO feedbacks
        return hash

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

    @staticmethod
    def filter(query, country=None, city=None, post_code=None, street=None, number=None, hotel=None):
        if country:
            query = query.filter(Address.country.ilike("%{}%".format(country)))
        if city:
            query = query.filter(Address.city.ilike("%{}%".format(city)))
        if post_code:
            query = query.filter(Address.post_code.ilike("%{}%".format(post_code)))
        if street:
            query = query.filter(Address.street.ilike("%{}%".format(street)))
        if number:
            query = query.filter(Address.number == number)
        if hotel:
            query = query.filter(Address.hotel == hotel)
        return query

    def serialize(self, hotel=False):
        hash = {
            'id': self.id,
            'country': self.country,
            'city': self.city,
            'post_code': self.post_code,
            'street': self.street,
            'number': self.number,
            'hotel_id': self.hotel_id,
        }
        if hotel:
            hash['hotel'] = self.hotel.serialize()
        return hash

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
    type        = db.Column(db.Integer, \
        CheckConstraint("type in (%s)" % (", ".join([str(t.value) for t in RoomType]))))
    description = db.Column(db.Text)

    hotel_id    = db.Column(db.Integer, \
        db.ForeignKey('hotels.id'))
    hotel       = db.relationship('Hotel', \
        back_populates='room_categories')

    rooms       = db.relationship('Room', \
        back_populates='room_category')

    def __init__(self, _type, _price, _hotel, _description):
        self.type  = _type
        self.price = _price
        self.hotel = _hotel
        self.description = _description

    def __repr__(self):
        return "<RoomCategory(type='%s', price='%s')>" \
            % (self.type, self.price)

    @staticmethod
    def subordinates_editable(query, current_user):
        # TODO opravneni
        query = query.join(Hotel, RoomCategory.hotel)
        return query

    # HOTEL, ROOMS means to include hotel and rooms
    def serialize(self, hotel=False, rooms=False):
        hash = {
            'id': self.id,
            'price': float(self.price),
            'type': RoomType(self.type).name,
            'description': self.description,
            'hotel_id': self.hotel_id,
        }
        if hotel:
            hash['hotel'] = self.hotel.serialize()
        if rooms:
            hash['rooms'] = []
            for room in self.rooms:
                hash['rooms'].append(room.serialize())
        return hash

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
            RoomType(self.room_category.type).name, self.room_category.price
            )

    @staticmethod
    def subordinates_editable(query, current_user):
        # TODO opravneni
        query = query.join(RoomCategory, Room.room_category)
        return query

    def serialize(self, room_category=False, reservations_rooms=False):
        hash = {
            'id': self.id,
            'number': self.number,
            'beds': self.beds,
            'room_category_id': self.room_category_id,
        }
        if room_category:
            hash['room_category'] = self.room_category.serialize()
        if reservations_rooms:
            hash['reservations_rooms'] = []
            for reservation_room in self.reservations_rooms:
                hash['reservations_rooms'].append(reservation_room.serialize())
        return hash

    @staticmethod
    def free_rooms_by_dates(date_from, date_to):
        rooms = Room.query.all()
        free_rooms = []
        for room in rooms:
            if not room.reservations_rooms:
                free_rooms.append(room)
            else:
                to_append = True
                for reservation_room in room.reservations_rooms:
                    if reservation_room.is_active:
                        if reservation_room.date_from >= date_from and reservation_room.date_from < date_to:
                            to_append = False
                            break
                        elif reservation_room.date_to > date_from and reservation_room.date_to < date_to:
                            to_append = False
                            break
                        elif reservation_room.date_from < date_from and reservation_room.date_to > date_to:
                            to_append = False
                            break
                if to_append:
                    free_rooms.append(room)
        return free_rooms

class ReservationRoom(db.Model):
    __tablename__  = 'reservations_rooms'

    id              = db.Column(db.Integer, primary_key=True)
    date_from       = db.Column(db.Date)
    date_to         = db.Column(db.Date)
    is_active       = db.Column(db.Boolean)

    room_id         = db.Column(db.Integer, \
        db.ForeignKey('rooms.id'))
    room            = db.relationship("Room", \
        back_populates="reservations_rooms")

    reservation_id  = db.Column(db.Integer, \
        db.ForeignKey('reservations.id'))
    reservation     = db.relationship("Reservation", \
        back_populates="reservations_rooms")

    def __init__(self, _date_from, _date_to, _is_active=True):
        self.date_from  = _date_from
        self.date_to    = _date_to
        self.is_active  = _is_active

    def __repr__(self):
        return "<ReservationRoom(date_from='%s', date_to='%s')>" \
            % (self.date_from, self.date_to)

    @staticmethod
    def filter(query, date_from=None, date_to=None, room_id=None, reservation_id=None, is_active=True):
        if date_from:
            query = query.filter(ReservationRoom.date_from >= date_from)
        if date_to:
            query = query.filter(ReservationRoom.date_from <= date_to)
        if room_id:
            query = query.filter(ReservationRoom.room_id == room_id)
        if reservation_id:
            query = query.filter(ReservationRoom.reservation_id == reservation_id)
        query = query.filter(ReservationRoom.is_active == is_active)
        return query 

    @staticmethod
    def join_Hotel(query):
        # TODO Need to use subordinates_editable for join
        query = query.join(Room, ReservationRoom.room).join(RoomCategory, Room.room_category).join(Hotel, RoomCategory.hotel)

    @staticmethod
    def subordinates_editable(query, current_user):
        if current_user.is_authenticated:
            if current_user.role == UserRole.ADMIN.value:
                pass
            elif current_user.role == UserRole.DIRECTOR.value:
                query = RoomCategory.join_Hotel(query)
                query = query.join(User, Hotel.owner)
                query = User.by_ids(query, [current_user.id])
            elif current_user.role == UserRole.RECEPTIONIST.value:
                query = RoomCategory.join_Hotel(query)
                query = query.join(User, Hotel.receptionists)
                query = User.by_ids(query, [current_user.id])
            else:
                # TODO ostatni
                query = query.filter(False)
        else:
            query = query.filter(False)
        return query

    def serialize(self, room=False, reservation=False, room_category=False):
        hash = {
            'id': self.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'is_active': self.is_active,
            'room_id': self.room_id,
            'reservation_id': self.reservation_id,
        }
        if room:
            hash['room'] = self.room.serialize(room_category=room_category)
        if reservation:
            hash['reservation'] = self.reservation.serialize()
        return hash

class Reservation(db.Model):
    __tablename__  = 'reservations'

    id              = db.Column(db.Integer, primary_key=True)

    reservations_rooms = db.relationship('ReservationRoom', \
        back_populates='reservation')

    payment_id      = db.Column(db.Integer, db.ForeignKey('payments.id'))
    payment         = db.relationship('Payment', \
        back_populates="reservation", \
        uselist=False)

    customer_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    customer        = db.relationship('User', \
        # foreign_keys = customer_id, \
        back_populates = 'customer_reservations')

    histories       = db.relationship("History", \
        back_populates="reservation")

    def __init__(self, _customer, _payment):
        self.customer       = _customer
        self.payment        = _payment

    def __repr__(self):
        return "<Reservation(id='%s', status='')>" \
            % (self.id,) #self.status)

    @staticmethod # -> query
    def filter(query, payment_id, customer_id):
        pass

    @staticmethod
    def join_Hotel(query):
        query = query.join(ReservationRoom, Reservation.reservations_rooms).join(Room, ReservationRoom.room)\
            .join(RoomCategory, Room.room_category).join(Hotel, RoomCategory.hotel)
        return query

    @staticmethod
    def subordinates_editable(query, current_user):
        # DIRECTOR -> reservations in hotels, which he owns
        # RECEPTIONIST -> reservations in hotels, where he is receptionist
        # CUSTOMER, ANON -> reservations, that he made
        if current_user.is_authenticated:
            if current_user.role == UserRole.ADMIN.value:
                pass
            elif current_user.role == UserRole.DIRECTOR.value:
                query = Reservation.join_Hotel(query)
                query = query.join(User, Hotel.owner)
                query = User.by_ids(query, [current_user.id])
            elif current_user.role == UserRole.RECEPTIONIST.value:
                query = Reservation.join_Hotel(query)
                query = query.join(User, Hotel.receptionists)
                query = User.by_ids(query, [current_user.id])
            else:
                query = query.filter(Reservation.customer_id == current_user.id)
        else:
            query = query.filter(False)
        return query

    def serialize(self, reservations_rooms=False, payment=False, customer=False, histories=False, room=False, room_category=False):
        hash = {
            'id': self.id,
            'payment_id': self.payment_id,
            'customer_id': self.customer_id,
            'status': self.last_status().name
        }
        if reservations_rooms:
            hash['reservations_rooms'] = []
            for reservation_room in self.reservations_rooms:
                hash['reservations_rooms'].append(reservation_room.serialize(room=room, room_category=room_category))
        if payment:
            hash['payment'] = self.payment.serialize()
        if customer:
            hash['customer'] = self.customer.serialize()
        if histories:
            hash['histories'] = []
            for history in self.histories:
                hash['histories'].append(history.serialize())
        return hash
    
    def last_status(self):
        if self.histories:
            return ReservationStatus(self.histories[-1].reservation_status)
        else:
            return ReservationStatus.NEW


class Payment(db.Model):
    __tablename__  = 'payments'

    id              = db.Column(db.Integer, primary_key=True)
    block_amount    = db.Column(db.Numeric)
    full_amount     = db.Column(db.Numeric)
    tax             = db.Column(db.Numeric)
    is_blocked      = db.Column(db.Boolean)
    is_paid        = db.Column(db.Boolean)

    reservation     = db.relationship("Reservation", \
        back_populates="payment")

    def __init__(self, _block_amount, _full_amount, _tax=None, _is_blocked=False, _is_paid=False):
        self.block_amount   = _block_amount
        self.full_amount    = _full_amount
        self.tax            = _tax
        self.is_blocked     = _is_blocked
        self.is_paid        = _is_paid

    def __repr__(self):
        return "<Payment(block_amount='%s', full_amount='%s', is_blocked='%s', is_paid='%s')>" \
            % (self.block_amount, self.full_amount, self.is_blocked, self.is_paid)

    def serialize(self, reservation=False):
        hash =  {
            'id': self.id,
            'block_amount': float(self.block_amount),
            'full_amount': float(self.full_amount),
            'tax': float(self.tax),
            'is_blocked': self.is_blocked,
            'is_paid': self.is_paid,
        }
        if reservation:
            hash['reservation'] = self.reservation.serialize()
        return hash

class History(db.Model):
    __tablename__  = 'histories'

    id                 = db.Column(db.Integer, primary_key=True)
    change_date        = db.Column(db.Date)

    reservation_status = db.Column(db.Integer, \
        CheckConstraint("reservation_status in (%s)" % (", ".join([str(s.value) for s in ReservationStatus]))))

    reservation_id     = db.Column(db.Integer, db.ForeignKey('reservations.id'))
    reservation        = db.relationship("Reservation", \
        back_populates="histories")

    receptionist_id    = db.Column(db.Integer, db.ForeignKey('users.id'))
    receptionist       = db.relationship("User", \
        back_populates="histories")

    def __init__(self, _reservation, _reservation_status, _change_date, _receptionist):
        self.reservation        = _reservation
        self.reservation_status = _reservation_status
        self.change_date        = _change_date
        self.receptionist       = _receptionist

    def __repr__(self):
        return "<History(reservation='%s', reservation_status='%s', change_date='%s', receptionist='%s')>" \
            % (self.reservation, self.reservation_status, self.change_date, self.receptionist)

    # @staticmehtod
    # def order_by(query, change_date):
    #     if change_date:
    #         query = query.order_by(History.change_date.desc())

    @staticmethod
    def filter(query, change_date, reservation_status, reservation_id, receptionist_id):
        # if change_data:
        #     query = query.filter(History.change_data <=)
        if reservation_status:
            query = query.filter(History.reservation_status == reservation_status)

    def serialize(self, reservation=False, receptionist=False):
        hash = {
            'id': self.id,
            'change_date': self.change_date,
            'reservation_status': {self.reservation_status: ReservationStatus(self.reservation_status).name},
        }
        if self.reservation:
            hash['reservation'] = self.reservation.serialize()
        if self.receptionist:
            hash['receptionist'] = self.receptionist.serialize()
        return hash