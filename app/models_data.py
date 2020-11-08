from app import db
from datetime import datetime, timedelta, date
from .models import User, Role, Feedback, Hotel, Status, Payment, Reservation, ReservationRoom, Room, RoomCategory #, Equipment

def load_models_data():
    print ('Inserting data')

    # ROLES
    # def __init__(self, _name):

    role_admin          = Role('ADMIN')
    role_director       = Role('DIRECTOR')
    role_receptionist   = Role('RECEPTIONIST')
    role_customer       = Role('CUSTOMER')
    role_anon           = Role('ANON')

    db.session.add_all([
        role_admin,
        role_director, role_receptionist,
        role_customer, role_anon
    ])

    # USERS
    # def __init__(self, _username, _password, _first_name, _last_name, _email, _birth_date, _role):

    # 1 ADMIN, 3 DIRECTORS; 4 RECEPTIONISTS, 8 CUSTOMERS
    admin_0 = User('admin_0', 'a_0_qwerty', 'Admin', 'Admin 0', 'admin@gmail.com', date(1980, 1, 1), role_admin)

    director_0 = User('director_0', 'd_0_qwerty', 'Ivan', 'Director 0', 'director_0@gmail.com', date(1981, 1, 1), role_director)
    director_1 = User('director_1', 'd_1_qwerty', 'Ivan', 'Director 1', 'director_1@gmail.com', date(1981, 2, 2), role_director)
    director_2 = User('director_2', 'd_2_qwerty', 'Ivan', 'Director 2', 'director_2@gmail.com', date(1981, 3, 3), role_director)

    receptionist_0 = User('receptionist_0', 'r_0_qwerty', 'Oleg', 'Receptionist 0', 'receptionist_0@gmail.com', date(1982, 1, 1), role_receptionist)
    receptionist_1 = User('receptionist_1', 'r_1_qwerty', 'Oleg', 'Receptionist 1', 'receptionist_1@gmail.com', date(1982, 2, 2), role_receptionist)
    receptionist_2 = User('receptionist_2', 'r_2_qwerty', 'Oleg', 'Receptionist 2', 'receptionist_2@gmail.com', date(1982, 3, 3), role_receptionist)
    receptionist_3 = User('receptionist_3', 'r_3_qwerty', 'Oleg', 'Receptionist 3', 'receptionist_3@gmail.com', date(1982, 4, 4), role_receptionist)

    customer_0 = User('customer_0', 'c_0_qwerty', 'Vasia', 'Customer 0', 'customer_0@gmail.com', date(1985, 1, 1), role_customer)
    customer_1 = User('customer_1', 'c_1_qwerty', 'Vasia', 'Customer 1', 'customer_1@gmail.com', date(1985, 2, 2), role_customer)
    customer_2 = User('customer_2', 'c_2_qwerty', 'Vasia', 'Customer 2', 'customer_2@gmail.com', date(1985, 3, 3), role_customer)
    customer_3 = User('customer_3', 'c_3_qwerty', 'Vasia', 'Customer 3', 'customer_3@gmail.com', date(1985, 4, 4), role_customer)

    customer_4 = User('customer_4', 'c_4_qwerty', 'Vasia', 'Customer 4', 'customer_4@gmail.com', date(1985, 5, 5), role_customer)
    customer_5 = User('customer_5', 'c_5_qwerty', 'Vasia', 'Customer 5', 'customer_5@gmail.com', date(1985, 6, 6), role_customer)
    customer_6 = User('customer_6', 'c_6_qwerty', 'Vasia', 'Customer 6', 'customer_6@gmail.com', date(1985, 7, 7), role_customer)
    customer_7 = User('customer_7', 'c_7_qwerty', 'Vasia', 'Customer 7', 'customer_7@gmail.com', date(1985, 8, 8), role_customer)

    db.session.add_all([
        admin_0,
        director_0, director_1, director_2,
        receptionist_0, receptionist_1, receptionist_2, receptionist_3,
        customer_0, customer_1, customer_2, customer_3,
        customer_4, customer_5, customer_6, customer_7,
    ])

    # HOTELS
    # def __init__(self, _name, _description, _stars, _address, _owner):

    hotel_0 = Hotel('Jizni Morava International',
        'Luxusni hotel v Brne pro podnikatele',
        5, 'Masarykova 1, Brno 602 00', director_0)

    hotel_1 = Hotel('Praha President Hotel',
        'Nejlepsi hotel v Praze pro prezidenty',
        4, 'Korunni 691, Praha-Vinohrady 120 00', director_1)

    hotel_2 = Hotel('Brno Grand Hotel',
        'Kolem hotelu je vzdycky hodne opilcu, bezdomovcu a vselijakych sebrancu',
        3, 'Benesova 605, Brno 602 00', director_2)

    db.session.add_all([hotel_0, hotel_1, hotel_2])

    # status1 = Status('created')
    # status2 = Status('booked')
    # status3 = Status('canceled')

    # db.session.add_all([status1, status2, status3])

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