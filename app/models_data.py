from app import db
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from .models import User, Feedback, Hotel, Address, Payment, Reservation, ReservationRoom, Room, \
    RoomCategory, UserRole, HotelStars, ReservationStatus, RoomType

def load_models_data():
    print ('Inserting data')

    # ROLES
    # def __init__(self, _name):

    # role_admin          = Role('ADMIN', 99)
    # role_director       = Role('DIRECTOR', 50)
    # role_receptionist   = Role('RECEPTIONIST', 25)
    # role_customer       = Role('CUSTOMER', 10)
    # role_anon           = Role('ANON', )

    # db.session.add_all([
    #     role_admin,
    #     role_director,
    #     role_receptionist,
    #     role_customer 
    #     #, role_anon
    # ])

    # USERS
    # def __init__(self, _username, _password, _first_name, _last_name, _email, _birth_date):

    # 1 ADMIN, 3 DIRECTORS; 4 RECEPTIONISTS, 8 CUSTOMERS
    admin_0 = User('Admin', 'Admin 0', 'admin@gmail.com', 'a0qwerty', UserRole.ADMIN.value)

    # ПОМЕНЯЛ ПАРОЛИ ЧТОБ БЫЛО УДОБНО ВВОДИТЬ. НИКАКИХ НИЖНИХ ДЕФИСОВ
    director_0 = User('Ivan', 'Director 0', 'director0@gmail.com', 'd0qwerty', UserRole.DIRECTOR.value)
    director_1 = User('Ivan', 'Director 1', 'director1@gmail.com', 'd1qwerty', UserRole.DIRECTOR.value)
    director_2 = User('Ivan', 'Director 2', 'director2@gmail.com', 'd2qwerty', UserRole.DIRECTOR.value)

    receptionist_0 = User('Oleg', 'Receptionist 0', 'receptionist0@gmail.com', 'r0qwerty', UserRole.RECEPTIONIST.value)
    receptionist_1 = User('Oleg', 'Receptionist 1', 'receptionist1@gmail.com', 'r1qwerty', UserRole.RECEPTIONIST.value)
    receptionist_2 = User('Oleg', 'Receptionist 2', 'receptionist2@gmail.com', 'r2qwerty', UserRole.RECEPTIONIST.value)
    receptionist_3 = User('Oleg', 'Receptionist 3', 'receptionist3@gmail.com', 'r3qwerty', UserRole.RECEPTIONIST.value)

    customer_0 = User('Vasia', 'Customer 0', 'customer0@gmail.com', 'c0qwerty', UserRole.CUSTOMER.value)
    customer_1 = User('Vasia', 'Customer 1', 'customer1@gmail.com', 'c1qwerty', UserRole.CUSTOMER.value)
    customer_2 = User('Vasia', 'Customer 2', 'customer2@gmail.com', 'c2qwerty', UserRole.CUSTOMER.value)
    customer_3 = User('Vasia', 'Customer 3', 'customer3@gmail.com', 'c3qwerty', UserRole.CUSTOMER.value)

    customer_4 = User('Vasia', 'Customer 4', 'customer4@gmail.com', 'c4qwerty', UserRole.CUSTOMER.value)
    customer_5 = User('Vasia', 'Customer 5', 'customer5@gmail.com', 'c5qwerty', UserRole.CUSTOMER.value)
    customer_6 = User('Vasia', 'Customer 6', 'customer6@gmail.com', 'c6qwerty', UserRole.CUSTOMER.value)
    customer_7 = User('Vasia', 'Customer 7', 'customer7@gmail.com', 'c7qwerty', UserRole.CUSTOMER.value)

    db.session.add_all([
        admin_0,
        director_0, director_1, director_2,
        receptionist_0, receptionist_1, receptionist_2, receptionist_3,
        customer_0, customer_1, customer_2, customer_3,
        customer_4, customer_5, customer_6, customer_7,
    ])

    address_0 = Address('Czech Republic', 'Brno', '602 00', 'Masarykova', '21')
    address_1 = Address('Czech Republic', 'Praha-Vinohrady', '120 00', 'Korunni', '691')
    address_2 = Address('Česká republika', 'Brno', '602 00', 'Benesova', '605')
    address_3 = Address('Česká republika', 'Praha 6', '165 00', 'Sídlištní', '1/1167')

    # HOTELS
    # def __init__(self, _name, _description, _stars, _address, _owner):

    hotel_0 = Hotel('Jizni Morava International',
        'Luxusni hotel v Brne pro podnikatele',
        HotelStars.FIVE.value, address_0, director_0)

    hotel_1 = Hotel('Praha President Hotel',
        'Nejlepsi hotel v Praze pro prezidenty',
        HotelStars.FOUR.value, address_1, director_1)

    hotel_2 = Hotel('Brno Grand Hotel',
        'Kolem hotelu je vzdycky hodne opilcu, bezdomovcu a vselijakych sebrancu',
        HotelStars.THREE.value, address_2, director_2)

    hotel_3 = Hotel('Prague Hotel Carl Inn Free Parking',
        "Prague Hotel Carl Inn Free Parking se nachází vedle autobusové zastávky "+
        "Kamýcká v klidné rezidenční čtvrti v Praze 6. "+
        "Nabízí restauraci, bar a bezplatné Wi-Fi připojení. "+
        "Každý pokoj má posezení, kabelovou TV, trezor, lednici a "+
        "vlastní koupelnu se sprchou a toaletními potřebami zdarma. "+
        "Vybrané pokoje mají balkon. "+
        " Prague Hotel Carl Inn Free Parking disponuje nepřetržitě otevřenou recepcí, "+
        "zahradou a terasou. Mezi poskytované služby patří prodej vstupenek, "+
        "turistické informace a bezplatná úschova zavazadel. "+
        "Na místě je neplacené parkoviště. Za příplatek mohou hosté využívat bazén, "+
        "tenisové kurty a fitness centrum, to vše vzdálené jen 50 metrů od hotelu. "+
        "Hotel se nachází 6 km od Pražského hradu a 7 km od letiště Václava Havla Praha. "+
        "Na požádání a za příplatek lze zajistit kyvadlovou dopravu.",
        HotelStars.FOUR.value, address_3, director_0)


    address_0.hotel_id = hotel_0.id
    address_1.hotel_id = hotel_1.id
    address_2.hotel_id = hotel_2.id
    address_3.hotel_id = hotel_3.id

    # db.session.add_all([status1, status2, status3])
    db.session.add_all([
        address_0, address_1, address_2, address_3,
        hotel_0, hotel_1, hotel_2, hotel_3
    ])

    # ROOMS_CATEORIES
    # def __init__(self, _type, _price, _hotel):

    room_cat_0_0 = RoomCategory(RoomType.LUX.value,      2500, hotel_0,
        "Luxusni pokoj")
    room_cat_0_1 = RoomCategory(RoomType.STANDARD.value, 2000, hotel_0,
        "Standardni pokoj na miru")

    room_cat_1_0 = RoomCategory(RoomType.LUX.value,      2000, hotel_1,
        "Luxusni pokoj Prestiz++")
    room_cat_1_1 = RoomCategory(RoomType.STANDARD.value, 1500, hotel_1,
        "Pokud nejste prezident -> tak standard")

    room_cat_2_0 = RoomCategory(RoomType.LUX.value,      1500, hotel_2,
        "Dokonaly lux s holky vevnitr")
    room_cat_2_1 = RoomCategory(RoomType.STANDARD.value, 1200, hotel_2,
        "Vyhodny standard")

    room_cat_3_0 = RoomCategory(RoomType.STANDARD.value, 2000, hotel_3,
        "Prazsky standard za Prazskou cenu")
    room_cat_3_1 = RoomCategory(RoomType.BUSINESS.value, 2500, hotel_3,
        "Urcen pro podnikave lidi")


    db.session.add_all([
        room_cat_0_0, room_cat_0_1,
        room_cat_1_0, room_cat_1_1,
        room_cat_2_0, room_cat_2_1,
        room_cat_3_0, room_cat_3_1,
    ])

    # ROOMS
    # def __init__(self, _number, _beds, _room_category):

    TWO_BEDS = 2
    THREE_BEDS = 3
    FOUR_BEDS = 4

    # 4 LUXY
    room_0_0_0 = Room(1, TWO_BEDS, room_cat_0_0)
    room_0_0_1 = Room(2, TWO_BEDS, room_cat_0_0)
    room_0_0_2 = Room(3, THREE_BEDS, room_cat_0_0)
    room_0_0_3 = Room(4, THREE_BEDS, room_cat_0_0)

    # 4 STANDARDY
    room_0_1_0 = Room(5, TWO_BEDS, room_cat_0_1)
    room_0_1_1 = Room(6, TWO_BEDS, room_cat_0_1)
    room_0_1_2 = Room(7, THREE_BEDS, room_cat_0_1)
    room_0_1_3 = Room(8, THREE_BEDS, room_cat_0_1)

    # 3 LUXY
    room_1_0_0 = Room(1, TWO_BEDS, room_cat_1_0)
    room_1_0_1 = Room(2, TWO_BEDS, room_cat_1_0)
    room_1_0_2 = Room(3, THREE_BEDS, room_cat_1_0)

    # 3 STANDARDY
    room_1_1_0 = Room(4, THREE_BEDS, room_cat_1_1)
    room_1_1_1 = Room(5, TWO_BEDS, room_cat_1_1)
    room_1_1_2 = Room(6, TWO_BEDS, room_cat_1_1)

    # 5 LUXU
    room_2_0_0 = Room(1, TWO_BEDS, room_cat_2_0)
    room_2_0_1 = Room(2, TWO_BEDS, room_cat_2_0)
    room_2_0_2 = Room(3, THREE_BEDS, room_cat_2_0)
    room_2_0_2 = Room(4, THREE_BEDS, room_cat_2_0)
    room_2_0_2 = Room(5, THREE_BEDS, room_cat_2_0)

    # 5 STANDARDU
    room_2_1_0 = Room(6, THREE_BEDS, room_cat_2_1)
    room_2_1_1 = Room(7, TWO_BEDS, room_cat_2_1)
    room_2_1_2 = Room(8, TWO_BEDS, room_cat_2_1)
    room_2_1_2 = Room(9, TWO_BEDS, room_cat_2_1)
    room_2_1_2 = Room(10, TWO_BEDS, room_cat_2_1)

    # 4 STANDARDY
    room_3_0_0 = Room(1, TWO_BEDS,      room_cat_3_0)
    room_3_0_1 = Room(2, THREE_BEDS,    room_cat_3_0)
    room_3_0_2 = Room(3, THREE_BEDS,    room_cat_3_0)
    room_3_0_3 = Room(4, FOUR_BEDS,     room_cat_3_0)

    # 3 BUISSNESY
    room_3_1_0 = Room(5, TWO_BEDS,    room_cat_3_1)
    room_3_1_1 = Room(6, TWO_BEDS,    room_cat_3_1)
    room_3_1_2 = Room(7, THREE_BEDS,  room_cat_3_1)


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
        room_3_0_0, room_3_0_1, room_3_0_2, room_3_0_3, room_3_1_0, room_3_1_1, room_3_1_2,
    ])

#####
    # сам юзер делают резервацу
    # - юзер устанавливает даты
    # - ты выдаешь свободные комнаты на эти даты (отсортированные по категориям, с кол-вом комнат)
    # - юзер выбирает комнату(ы) и жмет бронировать
    #     if not authenticated:
    #         anon = User(first_name, last_name, email, None, UserRole.ANON.value)

    #     payment = Payment() # full = for each room (room_category.price * days)
    #                             # block = 0.5 full
    #                             # is_paid, is_blocked = False, False
    #     reservation = Reservation(customer or anon, payment)
    #     status = History(reservation, ReservationStatus, date_change=today, receptionist=None)

    #     for room in rooms:
    #         reservation_room = ReservationRoom(from, to)
    #         reservation_room.room = room
    #         reservation.reservations_rooms.append(reservation_room)

    # Hotel.room_categories.rooms
    # rooms = filter(lambda r: is_free(r, date_from, date_to), rooms)
    # rooms.sort()
#####

    payment1 = Payment(21.44, 30.5, 4.08)
    payment2 = Payment(5.4, 10.5, 1.22)
    payment3 = Payment(18.8, 19.3, 1.08)

    db.session.add_all([payment1, payment2, payment3])

    reserv1 = Reservation(ReservationStatus.NEW.value, customer_0, payment1)
    reserv2 = Reservation(ReservationStatus.CHECKED_IN.value, customer_1, payment1)
    reserv3 = Reservation(ReservationStatus.NEW.value, customer_0, payment1)
    reserv4 = Reservation(ReservationStatus.CHECKED_IN.value, customer_1, payment2)
    reserv5 = Reservation(ReservationStatus.CHECKED_OUT.value, customer_2, payment3)
    reserv6 = Reservation(ReservationStatus.CHECKED_OUT.value, customer_3, payment3)
    reserv7 = Reservation(ReservationStatus.NEW.value, customer_0, payment2)

    res_room = ReservationRoom(datetime.today(), datetime.today() + timedelta(days=5))
    res_room.room = room_2_0_1
    reserv1.reservations_rooms.append(res_room)

    res_room = ReservationRoom(datetime.today(), datetime.today() + timedelta(days=5))
    res_room.room = room_1_0_2
    reserv1.reservations_rooms.append(res_room)

    res_room = ReservationRoom(datetime.today() - timedelta(days=7), datetime.today() - timedelta(days=1))
    res_room.room = room_1_0_2
    reserv2.reservations_rooms.append(res_room)

    res_room = ReservationRoom(datetime.today() + timedelta(days=2), datetime.today() + timedelta(days=5))
    res_room.room = room_1_0_0
    reserv3.reservations_rooms.append(res_room)

    res_room = ReservationRoom(datetime.today() - timedelta(days=10), datetime.today() - timedelta(days=5))
    res_room.room = room_2_0_1
    reserv4.reservations_rooms.append(res_room)
    res_room = ReservationRoom(datetime.today() + timedelta(days=1), datetime.today() + timedelta(days=7))
    res_room.room = room_2_0_2
    reserv4.reservations_rooms.append(res_room)

    res_room = ReservationRoom(datetime.today() - timedelta(days=15), datetime.today() - timedelta(days=9))
    res_room.room = room_0_0_2
    reserv5.reservations_rooms.append(res_room)

    res_room = ReservationRoom(datetime.today() - relativedelta(months=1, days=13), datetime.today() - relativedelta(months=1, days=9))
    res_room.room = room_0_1_1
    reserv6.reservations_rooms.append(res_room)

    res_room = ReservationRoom(datetime.today() + relativedelta(days=10), datetime.today() + relativedelta(days=13))
    res_room.room = room_1_0_2
    reserv7.reservations_rooms.append(res_room)

    db.session.add_all([
        reserv1,
        reserv2,
        reserv3,
        reserv4,
        reserv5
    ])

    print('Data inserted. Commit.')
    db.session.commit()
    print('OK. Committed.')
    db.session.close()