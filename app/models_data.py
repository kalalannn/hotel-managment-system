from app import db
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from .models import User, Feedback, Hotel, Address, Payment, Reservation, ReservationRoom, Room, \
    RoomCategory, UserRole, HotelStars, ReservationStatus, RoomType, History

def load_models_data():
    print ('Inserting data')

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

    db.session.add_all([
        room_0_0_0, room_0_0_1, room_0_0_2, room_0_0_3,
        room_0_1_0, room_0_1_1, room_0_1_2, room_0_1_3,
        room_1_0_0, room_1_0_1, room_1_0_2,
        room_1_1_0, room_1_1_1, room_1_1_2,
        room_2_0_0, room_2_0_1, room_2_0_2, room_2_0_2, room_2_0_2,
        room_2_1_0, room_2_1_1, room_2_1_2, room_2_1_2, room_2_1_2,
        room_3_0_0, room_3_0_1, room_3_0_2, room_3_0_3, room_3_1_0, room_3_1_1, room_3_1_2,
    ])

    # RESERVATION_0
    real_amount_0 = (room_cat_0_0.price + room_cat_0_1.price) * 6 # 6 days
    tax_0 = real_amount_0 * 0.21
    full_amount_0 = real_amount_0 + tax_0
    block_amount_0 = full_amount_0 * 0.5

    payment_0 = Payment(block_amount_0, full_amount_0, tax_0, True, True)
    reservation_0 = Reservation(customer_0, payment_0)

     # Datum v minulosti (2020-11-10)
    history_0_0 = History(reservation_0, ReservationStatus.NEW.value, date(2020, 11, 10), None)
    # Datum ODKDY "2020-11-15"
    history_0_1 = History(reservation_0, ReservationStatus.CHECKED_IN.value, date(2020, 11, 15), receptionist_0_1)
    # Datum DOKDY "2020-11-20"
    history_0_2 = History(reservation_0, ReservationStatus.CHECKED_OUT.value, date(2020, 11, 20), receptionist_0_2)
    res_room_0_0_0_0 = ReservationRoom("2020-11-15", "2020-11-20")
    res_room_0_0_0_0.room = room_0_0_0
    reservation_0.reservations_rooms.append(res_room_0_0_0_0)

    res_room_0_1_0_0 = ReservationRoom("2020-11-15", "2020-11-20")
    res_room_0_1_0_0.room = room_0_1_0
    reservation_0.reservations_rooms.append(res_room_0_1_0_0)

    db.session.add_all([payment_0, reservation_0, history_0_0, history_0_1, history_0_2, res_room_0_0_0_0, res_room_0_1_0_0])


    #RESERVATION_1
    real_amount_1 = (room_cat_1_0.price + room_cat_1_1.price) * 4 # 4 days
    tax_1 = real_amount_1 * 0.21
    full_amount_1 = real_amount_1 + tax_1
    block_amount_1 = full_amount_1 * 0.5

    payment_1 = Payment(block_amount_1, full_amount_1, tax_1, True, True)
    reservation_1 = Reservation(customer_1, payment_1)

    history_1_0 = History(reservation_1, ReservationStatus.NEW.value, date(2020, 11, 24), None)
    history_1_1 = History(reservation_1, ReservationStatus.CHECKED_IN.value, date(2020, 12, 1), receptionist_1_1)

    res_room_1_0_0_1 = ReservationRoom("2020-12-01", "2020-12-05")
    res_room_1_0_0_1.room = room_1_0_0
    reservation_1.reservations_rooms.append(res_room_1_0_0_1)

    res_room_1_1_0_1 = ReservationRoom("2020-12-01", "2020-12-05")
    res_room_1_1_0_1.room = room_1_1_0
    reservation_1.reservations_rooms.append(res_room_1_1_0_1)

    db.session.add_all([payment_1, reservation_1, history_1_0, history_1_1, res_room_1_0_0_1, res_room_1_1_0_1])

    #RESERVATION_2
    real_amount_2 = (room_cat_0_0.price + room_cat_0_1.price) * 5 # 5 days
    tax_2 = real_amount_2 * 0.21
    full_amount_2 = real_amount_2 + tax_2
    block_amount_2 = full_amount_2 * 0.5

    payment_2 = Payment(block_amount_2, full_amount_2, tax_2, True, True)
    reservation_2 = Reservation(customer_2, payment_2)

    history_2_0 = History(reservation_2, ReservationStatus.NEW.value, date(2020, 11, 11), None)
    history_2_1 = History(reservation_2, ReservationStatus.CHECKED_IN.value, date(2020, 12, 2), receptionist_0_1)

    res_room_1_0_0_2 = ReservationRoom("2020-12-02", "2020-12-07")
    res_room_1_0_0_2.room = room_1_0_1
    reservation_2.reservations_rooms.append(res_room_1_0_0_2)

    res_room_1_1_0_2 = ReservationRoom("2020-12-2", "2020-12-07")
    res_room_1_1_0_2.room = room_1_1_0
    reservation_2.reservations_rooms.append(res_room_1_1_0_2)

    db.session.add_all([payment_2, reservation_2, history_2_0, history_2_1, res_room_1_0_0_2, res_room_1_1_0_2])

        #RESERVATION_3
    real_amount_3 = (room_cat_2_0.price + room_cat_2_1.price) * 5 # 5 days
    tax_3 = real_amount_3 * 0.21
    full_amount_3 = real_amount_3 + tax_3
    block_amount_3 = full_amount_3 * 0.5

    payment_3 = Payment(block_amount_3, full_amount_3, tax_3, False, False)
    reservation_3 = Reservation(customer_3, payment_3)

    history_3_0 = History(reservation_3, ReservationStatus.NEW.value, date(2020, 1, 12), None)

    res_room_0_0_0_3 = ReservationRoom("2020-12-10", "2020-12-15")
    res_room_0_0_0_3.room = room_0_0_0
    reservation_3.reservations_rooms.append(res_room_0_0_0_3)

    res_room_0_1_1_3 = ReservationRoom("2020-12-10", "2020-12-15")
    res_room_0_1_1_3.room = room_2_1_0
    reservation_3.reservations_rooms.append(res_room_0_1_1_3)

    db.session.add_all([payment_3, reservation_3, history_3_0, res_room_0_0_0_3, res_room_0_1_1_3])

        #RESERVATION_4
    real_amount_4 = (room_cat_1_0.price + room_cat_1_1.price) * 8 # 8 days
    tax_4 = real_amount_4 * 0.21
    full_amount_4 = real_amount_4 + tax_4
    block_amount_4 = full_amount_4 * 0.5

    payment_4 = Payment(block_amount_4, full_amount_4, tax_4, True, False)
    reservation_4 = Reservation(customer_4, payment_4)

    history_4_0 = History(reservation_4, ReservationStatus.NEW.value, date(2020, 11, 29), None)

    res_room_0_0_0_4 = ReservationRoom("2020-12-11", "2020-12-19")
    res_room_0_0_0_4.room = room_0_0_0
    reservation_4.reservations_rooms.append(res_room_0_0_0_4)

    res_room_0_1_1_4 = ReservationRoom("2020-12-11", "2020-12-19")
    res_room_0_1_1_4.room = room_0_1_0
    reservation_4.reservations_rooms.append(res_room_0_1_1_4)

    db.session.add_all([payment_4, reservation_4, history_4_0, res_room_0_0_0_4, res_room_0_1_1_4])


        #RESERVATION_5
    real_amount_5 = (room_cat_3_0.price + room_cat_3_1.price) * 6 # 6 days
    tax_5 = real_amount_5 * 0.21
    full_amount_5 = real_amount_5 + tax_5
    block_amount_5 = full_amount_5 * 0.5

    payment_5 = Payment(block_amount_5, full_amount_5, tax_5, True, False)
    reservation_5 = Reservation(customer_5, payment_5)

    history_5_0 = History(reservation_5, ReservationStatus.NEW.value, date(2020, 11, 19), None)

    res_room_3_0_0_5 = ReservationRoom("2020-12-12", "2020-12-18")
    res_room_3_0_0_5.room = room_3_0_0
    reservation_5.reservations_rooms.append(res_room_3_0_0_5)

    res_room_3_1_0_5 = ReservationRoom("2020-12-12", "2020-12-18")
    res_room_3_1_0_5.room = room_3_1_0
    reservation_5.reservations_rooms.append(res_room_3_1_0_5)

    db.session.add_all([payment_5, reservation_5, history_5_0, res_room_3_0_0_5, res_room_3_1_0_5])



        #RESERVATION_6
    real_amount_6 = (room_cat_1_0.price + room_cat_1_1.price) * 6 # 6 days
    tax_6 = real_amount_0 * 0.21
    full_amount_6 = real_amount_6 + tax_6
    block_amount_6 = full_amount_6 * 0.5

    payment_6 = Payment(block_amount_6, full_amount_6, tax_6, True, True)
    reservation_6 = Reservation(customer_6, payment_6)

    history_6_0 = History(reservation_6, ReservationStatus.NEW.value, date(2020, 12, 1), None)
    res_room_1_0_0_6 = ReservationRoom("2020-12-21", "2020-12-29")
    res_room_1_0_0_6.room = room_1_0_0
    reservation_6.reservations_rooms.append(res_room_1_0_0_6)

    res_room_1_1_0_6 = ReservationRoom("2020-12-21", "2020-12-29")
    res_room_1_1_0_6.room = room_1_1_0
    reservation_6.reservations_rooms.append(res_room_1_1_0_6)

    db.session.add_all([payment_6, reservation_6, history_6_0, res_room_1_0_0_6, res_room_1_1_0_6])


        #RESERVATION_7
    real_amount_7 = (room_cat_2_0.price + room_cat_2_1.price) * 5 # 5 days
    tax_7 = real_amount_7* 0.21
    full_amount_7 = real_amount_7 + tax_7
    block_amount_7 = full_amount_7 * 0.5

    payment_7 = Payment(block_amount_7, full_amount_7, tax_7, True, True)
    reservation_7 = Reservation(customer_7, payment_7)

    history_7_0 = History(reservation_7, ReservationStatus.NEW.value, date(2020, 11, 23), None)
    history_7_1 = History(reservation_7, ReservationStatus.CHECKED_IN.value, date(2020, 12, 3), receptionist_2_1)

    res_room_2_0_0_7 = ReservationRoom("2020-12-03", "2020-12-08")
    res_room_2_0_0_7.room = room_2_0_0
    reservation_7.reservations_rooms.append(res_room_2_0_0_7)

    res_room_2_1_0_7 = ReservationRoom("2020-12-03", "2020-12-08")
    res_room_2_1_0_7.room = room_2_1_0
    reservation_7.reservations_rooms.append(res_room_2_1_0_7)

    db.session.add_all([payment_7, reservation_7, history_7_0, history_7_1, res_room_2_0_0_7, res_room_2_1_0_7])

    #RESERVATION_8
    real_amount_8 = (room_cat_2_0.price + room_cat_2_1.price) * 5 # 5 days
    tax_8 = real_amount_8* 0.21
    full_amount_8 = real_amount_8 + tax_8
    block_amount_8 = full_amount_8 * 0.5

    payment_8 = Payment(block_amount_8, full_amount_8, tax_8, True, True)
    reservation_8 = Reservation(customer_7, payment_8)

    history_8_0 = History(reservation_8, ReservationStatus.NEW.value, date(2020, 11, 1), None)
    history_8_1 = History(reservation_8, ReservationStatus.CHECKED_IN.value, date(2020, 11, 1), receptionist_2_1)
    history_8_2 = History(reservation_8, ReservationStatus.CHECKED_OUT.value, date(2020, 11, 6), receptionist_2_2)
    res_room_2_0_0_8 = ReservationRoom("2020-11-01", "2020-11-06")
    res_room_2_0_0_8.room = room_2_0_0
    reservation_8.reservations_rooms.append(res_room_2_0_0_8)

    res_room_2_1_0_8 = ReservationRoom("2020-11-01", "2020-11-06")
    res_room_2_1_0_8.room = room_2_1_0
    reservation_8.reservations_rooms.append(res_room_2_1_0_8)

    db.session.add_all([payment_8, reservation_8, history_8_0, history_8_1, history_8_2, res_room_2_0_0_8, res_room_2_1_0_8])

    #RESERVATION_9
    real_amount_9 = (room_cat_1_0.price + room_cat_1_1.price) * 5 # 5 days
    tax_9 = real_amount_9* 0.21
    full_amount_9 = real_amount_9 + tax_9
    block_amount_9 = full_amount_9 * 0.5

    payment_9 = Payment(block_amount_9, full_amount_9, tax_9, True, True)
    reservation_9 = Reservation(customer_3, payment_9)

    history_9_0 = History(reservation_9, ReservationStatus.NEW.value, date(2020, 11, 1), None)
    history_9_1 = History(reservation_9, ReservationStatus.CHECKED_IN.value, date(2020, 11, 1), receptionist_1_1)
    history_9_2 = History(reservation_9, ReservationStatus.CHECKED_OUT.value, date(2020, 11, 6), receptionist_1_2)
    res_room_1_0_0_9 = ReservationRoom("2020-11-01", "2020-11-06")
    res_room_1_0_0_9.room = room_1_0_0
    reservation_9.reservations_rooms.append(res_room_1_0_0_9)

    res_room_1_1_0_9 = ReservationRoom("2020-11-01", "2020-11-06")
    res_room_1_1_0_9.room = room_1_1_1
    reservation_9.reservations_rooms.append(res_room_1_1_0_9)

    db.session.add_all([payment_9, reservation_9, history_9_0, history_9_1, history_9_2, res_room_1_0_0_9, res_room_1_1_0_9])

    #RESERVATION_10
    real_amount_10 = (room_cat_3_0.price + room_cat_3_1.price) * 5 # 5 days
    tax_10 = real_amount_10* 0.21
    full_amount_10 = real_amount_10 + tax_10
    block_amount_10 = full_amount_10 * 0.5

    payment_10 = Payment(block_amount_10, full_amount_10, tax_10, True, True)
    reservation_10 = Reservation(customer_2, payment_10)

    history_10_0 = History(reservation_10, ReservationStatus.NEW.value, date(2020, 11, 1), None)
    history_10_1 = History(reservation_10, ReservationStatus.CHECKED_IN.value, date(2020, 11, 2), receptionist_3_1)
    history_10_2 = History(reservation_10, ReservationStatus.CHECKED_OUT.value, date(2020, 11, 7), receptionist_3_2)
    res_room_3_0_0_10 = ReservationRoom("2020-11-02", "2020-11-07")
    res_room_3_0_0_10.room = room_3_0_0
    reservation_10.reservations_rooms.append(res_room_3_0_0_10)

    res_room_3_1_1_10 = ReservationRoom("2020-11-02", "2020-11-07")
    res_room_3_1_1_10.room = room_3_1_1
    reservation_10.reservations_rooms.append(res_room_3_1_1_10)

    db.session.add_all([payment_10, reservation_10, history_10_0, history_10_1, history_10_2, res_room_3_0_0_10, res_room_3_1_1_10])

    #RESERVATION_11
    real_amount_11 = (room_cat_3_0.price + room_cat_3_1.price) * 5 # 5 days
    tax_11 = real_amount_11* 0.21
    full_amount_11 = real_amount_11 + tax_11
    block_amount_11 = full_amount_11 * 0.5

    payment_11 = Payment(block_amount_11, full_amount_11, tax_11, True, False)
    reservation_11 = Reservation(customer_6, payment_11)

    history_11_0 = History(reservation_11, ReservationStatus.NEW.value, date(2020, 11, 1), None)
    history_11_1 = History(reservation_11, ReservationStatus.CHECKED_IN.value, date(2020, 11, 2), receptionist_3_1)

    res_room_3_0_0_11 = ReservationRoom("2020-12-02", "2020-12-07")
    res_room_3_0_0_11.room = room_3_0_0
    reservation_11.reservations_rooms.append(res_room_3_0_0_11)

    res_room_3_1_1_11 = ReservationRoom("2020-12-02", "2020-12-07")
    res_room_3_1_1_11.room = room_3_1_1
    reservation_11.reservations_rooms.append(res_room_3_1_1_11)

    db.session.add_all([payment_11, reservation_11, history_11_0, history_11_1, res_room_3_0_0_11, res_room_3_1_1_11])

    # db.session.add_all([payment_0, payment_1, payment_2])

    # payment_1 = Payment(5.4, 10.5, 1.22)
    # payment_2 = Payment(18.8, 19.3, 1.08)

    # room_0_0_0 = Room(1, TWO_BEDS, room_cat_0_0)
    # room_0_1_0 = Room(5, TWO_BEDS, room_cat_0_1)

    # room_cat_0_0 = RoomCategory(RoomType.LUX.value,      2500, hotel_0,
    # room_cat_0_1 = RoomCategory(RoomType.STANDARD.value, 2000, hotel_0,

    # reservation_1 = Reservation(customer_0, payment_1)
    # reservation_2 = Reservation(customer_1, payment_1)
    # reservation_3 = Reservation(customer_0, payment_1)
    # reservation_4 = Reservation(customer_1, payment_2)
    # reservation_5 = Reservation(customer_2, payment_3)
    # reservation_6 = Reservation(customer_3, payment_3)
    # reservation_7 = Reservation(customer_0, payment_2)

    # res_room = ReservationRoom("2020-11-20", "2020-12-05")
    # res_room.room = room_1_0_2
    # reservation_2.reservations_rooms.append(res_room)

    # res_room = ReservationRoom("2020-12-9", "2020-12-15")
    # res_room.room = room_1_0_0
    # reservation_3.reservations_rooms.append(res_room)

    # res_room = ReservationRoom("2020-11-21", "2020-11-29")
    # res_room.room = room_2_0_1
    # reservation_4.reservations_rooms.append(res_room)

    # res_room = ReservationRoom("2020-11-30", "2020-12-11")
    # res_room.room = room_2_0_2
    # reservation_4.reservations_rooms.append(res_room)

    # res_room = ReservationRoom("2020-12-12", "2020-12-16")
    # res_room.room = room_0_0_2
    # reservation_5.reservations_rooms.append(res_room)

    # res_room = ReservationRoom("2020-12-21", "2020-12-27")
    # res_room.room = room_0_1_1
    # reservation_6.reservations_rooms.append(res_room)

    # res_room = ReservationRoom("2020-12-14", "2020-12-23")
    # res_room.room = room_1_0_2
    # reservation_7.reservations_rooms.append(res_room)

    #db.session.add_all([
    #    # reservation_0,
    #    # reservation_1,
    #    # reservation_2,
    #    # reservation_3,
    #    # reservation_4,
    #    # reservation_5
    #])

    print('Data inserted. Commit.')
    db.session.commit()
    print('OK. Committed.')
    db.session.close()