from app import db
from datetime import datetime, timedelta, date
from .models import User, Role, Feedback, Hotel, Status, Address, Payment, Reservation, ReservationRoom, Room, RoomCategory

def load_models_data():
    print ('Inserting data')

    # ROLES
    # def __init__(self, _name):

    role_admin          = Role('ADMIN', 99)
    role_director       = Role('DIRECTOR', 50)
    role_receptionist   = Role('RECEPTIONIST', 25)
    role_customer       = Role('CUSTOMER', 10)
    # role_anon           = Role('ANON', )

    db.session.add_all([
        role_admin,
        role_director, role_receptionist,
        role_customer #, role_anon
    ])

    # USERS
    # def __init__(self, _username, _password, _first_name, _last_name, _email, _birth_date):

    # 1 ADMIN, 3 DIRECTORS; 4 RECEPTIONISTS, 8 CUSTOMERS
    admin_0 = User('Admin', 'Admin 0', 'admin@gmail.com', 'a_0_qwerty',role_admin)

    director_0 = User('Ivan', 'Director 0', 'director_0@gmail.com', 'd_0_qwerty', role_director)
    director_1 = User('Ivan', 'Director 1', 'director_1@gmail.com', 'd_1_qwerty', role_director)
    director_2 = User('Ivan', 'Director 2', 'director_2@gmail.com', 'd_2_qwerty', role_director)

    receptionist_0 = User('Oleg', 'Receptionist 0', 'receptionist_0@gmail.com', 'r_0_qwerty', role_receptionist)
    receptionist_1 = User('Oleg', 'Receptionist 1', 'receptionist_1@gmail.com', 'r_1_qwerty', role_receptionist)
    receptionist_2 = User('Oleg', 'Receptionist 2', 'receptionist_2@gmail.com', 'r_2_qwerty', role_receptionist)
    receptionist_3 = User('Oleg', 'Receptionist 3', 'receptionist_3@gmail.com', 'r_3_qwerty', role_receptionist)

    customer_0 = User('Vasia', 'Customer 0', 'customer_0@gmail.com', 'c_0_qwerty', role_customer)
    customer_1 = User('Vasia', 'Customer 1', 'customer_1@gmail.com', 'c_1_qwerty', role_customer)
    customer_2 = User('Vasia', 'Customer 2', 'customer_2@gmail.com', 'c_2_qwerty', role_customer)
    customer_3 = User('Vasia', 'Customer 3', 'customer_3@gmail.com', 'c_3_qwerty', role_customer)

    customer_4 = User('Vasia', 'Customer 4', 'customer_4@gmail.com', 'c_4_qwerty', role_customer)
    customer_5 = User('Vasia', 'Customer 5', 'customer_5@gmail.com', 'c_5_qwerty', role_customer)
    customer_6 = User('Vasia', 'Customer 6', 'customer_6@gmail.com', 'c_6_qwerty', role_customer)
    customer_7 = User('Vasia', 'Customer 7', 'customer_7@gmail.com', 'c_7_qwerty', role_customer)

    db.session.add_all([
        admin_0,
        director_0, director_1, director_2,
        receptionist_0, receptionist_1, receptionist_2, receptionist_3,
        customer_0, customer_1, customer_2, customer_3,
        customer_4, customer_5, customer_6, customer_7,
    ])

    address_0 = Address('Czech Republic', 'Brno', '602 00', 'Masarykova', '21')
    address_1 = Address('Czech Republic', 'Praha-Vinohrady', '120 00', 'Korunni', '691')
    address_2 = Address('Czech Republic', 'Brno', '602 00', 'Benesova', '605')

    # HOTELS
    # def __init__(self, _name, _description, _stars, _address, _owner):

    hotel_0 = Hotel('Jizni Morava International',
        'Luxusni hotel v Brne pro podnikatele',
        5, address_0, director_0)

    hotel_1 = Hotel('Praha President Hotel',
        'Nejlepsi hotel v Praze pro prezidenty',
        4, address_1, director_1)

    hotel_2 = Hotel('Brno Grand Hotel',
        'Kolem hotelu je vzdycky hodne opilcu, bezdomovcu a vselijakych sebrancu',
        3, address_2, director_2)

    address_0.hotel_id = hotel_0.id
    address_1.hotel_id = hotel_1.id
    address_2.hotel_id = hotel_2.id

    db.session.add_all([
        address_0, address_1, address_2,
        hotel_0, hotel_1, hotel_2
    ])

    # payment1 = Payment(21.44, 30.5, 4.08)
    # payment2 = Payment(5.4, 10.5, 1.22)
    # payment3 = Payment(18.8, 19.3, 1.08)

    # db.session.add_all([payment1, payment2, payment3])

    # ROOMS_CATEORIES
    # def __init__(self, _type, _price, _hotel):

    room_cat_0_0 = RoomCategory('LUX',      2500, hotel_0)
    room_cat_0_1 = RoomCategory('STANDARD', 2000, hotel_0)

    room_cat_1_0 = RoomCategory('LUX',      2000, hotel_1)
    room_cat_1_1 = RoomCategory('STANDARD', 1500, hotel_1)

    room_cat_2_0 = RoomCategory('LUX',      1500, hotel_2)
    room_cat_2_1 = RoomCategory('STANDARD', 1200, hotel_2)

    db.session.add_all([
        room_cat_0_0, room_cat_0_1,
        room_cat_1_0, room_cat_1_1,
        room_cat_2_0, room_cat_2_1,
    ])

    # ROOMS
    # def __init__(self, _number, _beds, _room_category):

    DVA_LUZKA = 2
    TRI_LUZKA = 3

    # 4 LUXY
    room_0_0_0 = Room(DVA_LUZKA, 1, room_cat_0_0)
    room_0_0_1 = Room(DVA_LUZKA, 2, room_cat_0_0)
    room_0_0_2 = Room(TRI_LUZKA, 3, room_cat_0_0)
    room_0_0_3 = Room(TRI_LUZKA, 4, room_cat_0_0)

    # 4 STANDARDY
    room_0_1_0 = Room(DVA_LUZKA, 5, room_cat_0_1)
    room_0_1_1 = Room(DVA_LUZKA, 6, room_cat_0_1)
    room_0_1_2 = Room(TRI_LUZKA, 7, room_cat_0_1)
    room_0_1_3 = Room(TRI_LUZKA, 8, room_cat_0_1)

    # 3 LUXY
    room_1_0_0 = Room(DVA_LUZKA, 1, room_cat_1_0)
    room_1_0_1 = Room(DVA_LUZKA, 2, room_cat_1_0)
    room_1_0_2 = Room(TRI_LUZKA, 3, room_cat_1_0)

    # 3 STANDARDY
    room_1_1_0 = Room(TRI_LUZKA, 4, room_cat_1_1)
    room_1_1_1 = Room(DVA_LUZKA, 5, room_cat_1_1)
    room_1_1_2 = Room(DVA_LUZKA, 6, room_cat_1_1)

    # 5 LUXU
    room_2_0_0 = Room(DVA_LUZKA, 1, room_cat_2_0)
    room_2_0_1 = Room(DVA_LUZKA, 2, room_cat_2_0)
    room_2_0_2 = Room(TRI_LUZKA, 3, room_cat_2_0)
    room_2_0_2 = Room(TRI_LUZKA, 4, room_cat_2_0)
    room_2_0_2 = Room(TRI_LUZKA, 5, room_cat_2_0)

    # 5 STANDARDU
    room_2_1_0 = Room(TRI_LUZKA, 6, room_cat_2_1)
    room_2_1_1 = Room(DVA_LUZKA, 7, room_cat_2_1)
    room_2_1_2 = Room(DVA_LUZKA, 8, room_cat_2_1)
    room_2_1_2 = Room(DVA_LUZKA, 9, room_cat_2_1)
    room_2_1_2 = Room(DVA_LUZKA, 10,room_cat_2_1)

    # EQUIPMENT
    # def __init__(self, _type, _name):

    # sofa_0  = Equipment('LUX',      'sofa')
    # sofa_0  = Equipment('STANDARD', 'sofa')

    # tv_0    = Equipment('LUX',      'TV')
    # tv_1    = Equipment('STANDARD', 'TV')

    # fridge_0 = Equipment('LUX',      'fridge')
    # fridge_1 = Equipment('STANDARD', 'fridge')

    # db.session.add_all([eq1, eq2, eq3])

    # room1.equipments.extend([eq2, eq3])
    # room2.equipments.extend([eq1, eq3])

    db.session.add_all([
        room_0_0_0, room_0_0_1, room_0_0_2, room_0_0_3,
        room_0_1_0, room_0_1_1, room_0_1_2, room_0_1_3,
        room_1_0_0, room_1_0_1, room_1_0_2,
        room_1_1_0, room_1_1_1, room_1_1_2,
        room_2_0_0, room_2_0_1, room_2_0_2, room_2_0_2, room_2_0_2,
        room_2_1_0, room_2_1_1, room_2_1_2, room_2_1_2, room_2_1_2,
    ])

    # reserv1 = Reservation(status1, user1, user3, payment1)
    # res_room = ReservationRoom(datetime.today(), datetime.today() + timedelta(days=5))
    # res_room.room = room2
    # reserv1.rooms.append(res_room)
    # res_room = ReservationRoom(datetime.today() + timedelta(days=7), datetime.today() + timedelta(days=18))
    # res_room.room = room3
    # reserv1.rooms.append(res_room)
    # db.session.add(reserv1)

    # reserv2 = Reservation(status2, user1, user2, payment1)
    # res_room = ReservationRoom(datetime.today() + timedelta(days=10), datetime.today() + timedelta(days=22))
    # res_room.room = room3
    # reserv2.rooms.append(res_room)

    # db.session.add(reserv2)

    # reserv3 = Reservation(status3, user3, user3, payment3)
    # res_room = ReservationRoom(datetime.today() + timedelta(days=1), datetime.today() + timedelta(days=2))
    # res_room.room = room1
    # reserv3.rooms.append(res_room)

    # res_room = ReservationRoom(datetime.today() + timedelta(days=2), datetime.today() + timedelta(days=3))
    # res_room.room = room2
    # reserv3.rooms.append(res_room)

    # db.session.add(reserv3)

    print('Data inserted. Commit.')
    db.session.commit()
    print('OK. Committed.')
    db.session.close()