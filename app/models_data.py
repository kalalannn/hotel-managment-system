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
    admin_0 = User('Martin', 'Admin 0', 'admin@gmail.com', 'a0qwerty', UserRole.ADMIN.value)

    # ПОМЕНЯЛ ПАРОЛИ ЧТОБ БЫЛО УДОБНО ВВОДИТЬ. НИКАКИХ НИЖНИХ ДЕФИСОВ
    director_0 = User('Jan', 'Director 0', 'director0@gmail.com', 'd0qwerty', UserRole.DIRECTOR.value)
    director_1 = User('Jiří', 'Director 1', 'director1@gmail.com', 'd1qwerty', UserRole.DIRECTOR.value)
    director_2 = User('Jana', 'Director 2', 'director2@gmail.com', 'd2qwerty', UserRole.DIRECTOR.value)

    customer_0 = User('Pavel', 'Customer 0', 'customer0@gmail.com', 'c0qwerty', UserRole.CUSTOMER.value)
    customer_1 = User('Marie', 'Customer 1', 'customer1@gmail.com', 'c1qwerty', UserRole.CUSTOMER.value)
    customer_2 = User('Martin', 'Customer 2', 'customer2@gmail.com', 'c2qwerty', UserRole.CUSTOMER.value)
    customer_3 = User('Petr', 'Customer 3', 'customer3@gmail.com', 'c3qwerty', UserRole.CUSTOMER.value)

    customer_4 = User('Hana', 'Customer 4', 'customer4@gmail.com', 'c4qwerty', UserRole.CUSTOMER.value)
    customer_5 = User('Eva', 'Customer 5', 'customer5@gmail.com', 'c5qwerty', UserRole.CUSTOMER.value)
    customer_6 = User('Michal', 'Customer 6', 'customer6@gmail.com', 'c6qwerty', UserRole.CUSTOMER.value)
    customer_7 = User('Josef', 'Customer 7', 'customer7@gmail.com', 'c7qwerty', UserRole.CUSTOMER.value)

    db.session.add_all([
        admin_0,
        director_0, director_1, director_2,
        customer_0, customer_1, customer_2, customer_3,
        customer_4, customer_5, customer_6, customer_7,
    ])

    address_0 = Address('Česká republika', 'Brno', '602 00', 'Masarykova', '21')
    address_1 = Address('Česká republika', 'Praha-Vinohrady', '120 00', 'Korunni', '691')
    address_2 = Address('Česká republika', 'Brno', '602 00', 'Benesova', '605')
    address_3 = Address('Česká republika', 'Praha 6', '165 00', 'Sídlištní', '1/1167')

    # HOTELS
    # def __init__(self, _name, _description, _stars, _address, _owner):

    hotel_0 = Hotel('Jizni Morava International',
        "Hotel se nachází v centru města, na Šilingrově náměstí. Je umístěný v prestižní "+
        "historické budově. Hosté tu mohou zdarma využívat saunu, relaxační zónu a moderní fitness centrum."+
        "Ve všech prostorách je zdarma dostupné Wi-Fi. Jen pár kroků od ubytování najdete celou řadu historických památek "+
        "včetně katedrály sv. Petra a Pavla či hradu Špilberk. Jedinečně zařízené pokoje a apartmá vám zajistí "+
        "pohodlí pro ničím nerušený spánek. Všechny mají příslušenství pro přípravu čaje a kávy, minibar, fén, "+
        "kosmetické zrcátko, trezor, Wi-Fi, nabídku polštářů, žehličku a žehlicí prkno. Některé lze propojit a vytvořit tak velký rodinný apartmán.",
        HotelStars.FIVE.value, address_0, director_0)

    receptionist_0_1 = User('Oleg',  'JM Receptionist 1', 'JMreceptionist1@gmail.com', 'JMr1qwerty', UserRole.RECEPTIONIST.value, True, hotel_0)
    receptionist_0_2 = User('Petra', 'JM Receptionist 2', 'JMreceptionist2@gmail.com', 'JMr2qwerty', UserRole.RECEPTIONIST.value, True, hotel_0)

    hotel_1 = Hotel('Praha President Hotel',
        "Tento moderní business hotel stojí na břehu Vltavy v historickém centru Prahy." +
        "Prostorné a elegantně zařízené pokoje v hotelu President mají klimatizaci, minibar, posezení, "+
        "satelitní TV a výhled na Pražský hrad, na řeku nebo na historické centrum města." +
        "V restauraci hotelu se každé ráno podává snídaně. Hotel President stojí v bezprostřední "+
        "blízkosti židovské čtvrti a Pařížské ulice, 1 minutu chůze od historického centra města.",
        HotelStars.FOUR.value, address_1, director_1)

    receptionist_1_1 = User('Martin', 'PP Receptionist 1', 'PPreceptionist1@gmail.com', 'PPr1qwerty', UserRole.RECEPTIONIST.value, True, hotel_1)
    receptionist_1_2 = User('Jirka',  'PP Receptionist 2', 'PPreceptionist2@gmail.com', 'PPr2qwerty', UserRole.RECEPTIONIST.value, True, hotel_1)

    hotel_2 = Hotel('Brno Grand Hotel',
        "Tento hotel s dlouhou 140letou tradicí na poli pohostinství stojí ve středu malebného historického centra Brna, "+
        "v blízkosti všech hlavních památek, a jeho součástí je Garden Restaurant Le Grand připravující pokrmy české a "+
        "mezinárodní kuchyně i lobby bar s nabídkou nápojů a lehkého občerstvení.",
        HotelStars.THREE.value, address_2, director_2)

    receptionist_2_1 = User('Honza',     'BG Receptionist 1', 'BGreceptionist1@gmail.com', 'BGr1qwerty', UserRole.RECEPTIONIST.value, True, hotel_2)
    receptionist_2_2 = User('Katarina',  'BG Receptionist 2', 'BGreceptionist2@gmail.com', 'BGr2qwerty', UserRole.RECEPTIONIST.value, True, hotel_2)

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

    receptionist_3_1 = User('Marek',     'PH Receptionist 1', 'PHreceptionist1@gmail.com', 'PHr1qwerty', UserRole.RECEPTIONIST.value, True, hotel_3)
    receptionist_3_2 = User('Iveta',     'PH Receptionist 2', 'PHreceptionist2@gmail.com', 'PHr2qwerty', UserRole.RECEPTIONIST.value, True, hotel_3)

    address_0.hotel_id = hotel_0.id
    address_1.hotel_id = hotel_1.id
    address_2.hotel_id = hotel_2.id
    address_3.hotel_id = hotel_3.id

    # db.session.add_all([status1, status2, status3])
    db.session.add_all([
        address_0, address_1, address_2, address_3,
        hotel_0, hotel_1, hotel_2, hotel_3
    ])

    db.session.add_all([
        receptionist_0_1, receptionist_0_2,
        receptionist_1_1, receptionist_1_2,
        receptionist_2_1, receptionist_2_2,
        receptionist_3_1, receptionist_3_2,
    ])


    # ROOMS_CATEORIES
    # def __init__(self, _type, _price, _hotel):

    room_cat_0_0 = RoomCategory(RoomType.LUX.value,      2500, hotel_0,
        "Elegantní pokoj s klimatizací, zdarma dostupným Wi-Fi a bezplatným vstupem do sauny a fitness centra. ")
    room_cat_0_1 = RoomCategory(RoomType.STANDARD.value, 2000, hotel_0,
        "Tyto klimatizované pokoje jsou vybavené satelitní TV s plochou obrazovkou a minibarem.")

    room_cat_1_0 = RoomCategory(RoomType.LUX.value,      2000, hotel_1,
        "Pokoj s panoramatickým výhledem na město a vstupem do Executive Lounge a wellness ")
    room_cat_1_1 = RoomCategory(RoomType.STANDARD.value, 1500, hotel_1,
        "Pokoj s volným vstupem do zoo")

    room_cat_2_0 = RoomCategory(RoomType.LUX.value,      1500, hotel_2,
        "Prostorná apartmá s individuálně nastavitelnou klimatizací, satelitní TV s plochou obrazovkou, minibarem, "+
        "příslušenstvím pro přípravu čaje a kávy, trezorem a psacím stolem." +
        "Na vyžádání a dle dostupnosti je k dispozici apartmá s balkonem. ")
    room_cat_2_1 = RoomCategory(RoomType.STANDARD.value, 1200, hotel_2,
        "Tyto prostorné apartma mají obývací pokoj, Wi-Fi, příslušenství pro přípravu kávy a čaje.")

    room_cat_3_0 = RoomCategory(RoomType.STANDARD.value, 2000, hotel_3,
        "Užijte si pohodlný pobyt v tomto světlém pokoji s velkými okny")
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

    res_room = ReservationRoom("2020-12-01", "2020-12-06")
    res_room.room = room_2_0_1
    reserv1.reservations_rooms.append(res_room)

    res_room = ReservationRoom("2020-12-06", "2020-12-10")
    res_room.room = room_1_0_2
    reserv1.reservations_rooms.append(res_room)

    res_room = ReservationRoom("2020-11-20", "2020-12-05")
    res_room.room = room_1_0_2
    reserv2.reservations_rooms.append(res_room)

    res_room = ReservationRoom("2020-12-9", "2020-12-15")
    res_room.room = room_1_0_0
    reserv3.reservations_rooms.append(res_room)

    res_room = ReservationRoom("2020-11-21", "2020-11-29")
    res_room.room = room_2_0_1
    reserv4.reservations_rooms.append(res_room)
    res_room = ReservationRoom("2020-11-30", "2020-12-11")
    res_room.room = room_2_0_2
    reserv4.reservations_rooms.append(res_room)

    res_room = ReservationRoom("2020-12-12", "2020-12-16")
    res_room.room = room_0_0_2
    reserv5.reservations_rooms.append(res_room)

    res_room = ReservationRoom("2020-12-21", "2020-12-27")
    res_room.room = room_0_1_1
    reserv6.reservations_rooms.append(res_room)

    res_room = ReservationRoom("2020-12-14", "2020-12-23")
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