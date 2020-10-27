from app import db
from datetime import datetime, timedelta
from .models import User, Role, Feedback, Hotel, Status, Payment, Reservation, ReservationRoom, Room, RoomCategory, Equipment

def load_models_data():
    print ('Inserting data')

    role1 = Role('admin')
    role2 = Role('manager')
    role3 = Role('user')
    db.session.add_all([role1, role2, role3])
    db.session.commit()

    user1 = User('vasia007', '7juj', 'Vasia', 'Pupkin', 'vas_pup@mail.ru', datetime.today(), role2)
    user2 = User('kloun', 'asdfasdf', 'Klounito', 'Shapito', 'kla@lol', datetime.today(), role3)
    user3 = User('kalalannn', 'chapka*taschit', 'Nikolaj', 'Vorobiev', 'nik_vorob@gmail.com', datetime.today(), role1)
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    hotel1 = Hotel('Veveri', 'Hezky hotel', 4, 'vever. bityska 4', user1)
    hotel2 = Hotel('Zamek', 'pekny vikend', 3, 'brno namesti republiky 8', user3)
    hotel3 = Hotel('International', 'what the fuck', 5, 'minsk prospekt 34', user1)
    db.session.add_all([hotel1, hotel2, hotel3])
    db.session.commit()

    status1 = Status('created')
    status2 = Status('booked')
    status3 = Status('canceled')
    db.session.add_all([status1, status2, status3])
    db.session.commit()

    payment1 = Payment(21.44, 30.5, 4.08)
    payment2 = Payment(5.4, 10.5, 1.22)
    payment3 = Payment(18.8, 19.3, 1.08)
    db.session.add_all([payment1, payment2, payment3])
    db.session.commit()

    roomcat1 = RoomCategory('lux', 110, hotel1)
    roomcat2 = RoomCategory('delux', 130, hotel1)
    roomcat3 = RoomCategory('business', 90, hotel2)
    roomcat4 = RoomCategory('normal', 50, hotel2)
    roomcat5 = RoomCategory('poor', 30, hotel2)
    db.session.add_all([roomcat1, roomcat2, roomcat3, roomcat4, roomcat5])
    db.session.commit()

    room1 = Room(2, roomcat2)
    room2 = Room(3, roomcat2)
    room3 = Room(4, roomcat3)
    room4 = Room(4, roomcat4)
    room5 = Room(5, roomcat5)
    room6 = Room(6, roomcat5)
    db.session.add_all([room1, room2, room3, room4, room5, room6])
    db.session.commit()

    reserv1 = Reservation(status1, user1, user3, payment1)
    res_room = ReservationRoom(datetime.today(), datetime.today() + timedelta(days=5))
    res_room.room = room2
    reserv1.rooms.append(res_room)
    res_room = ReservationRoom(datetime.today() + timedelta(days=7), datetime.today() + timedelta(days=18))
    res_room.room = room3
    reserv1.rooms.append(res_room)
    db.session.add(reserv1)
    db.session.commit()

    reserv2 = Reservation(status2, user1, user2, payment1)
    res_room = ReservationRoom(datetime.today() + timedelta(days=10), datetime.today() + timedelta(days=22))
    res_room.room = room3
    reserv2.rooms.append(res_room)
    db.session.add(reserv2)
    db.session.commit()

    reserv3 = Reservation(status3, user3, user3, payment3)
    res_room = ReservationRoom(datetime.today() + timedelta(days=1), datetime.today() + timedelta(days=2))
    res_room.room = room1
    reserv3.rooms.append(res_room)
    res_room = ReservationRoom(datetime.today() + timedelta(days=2), datetime.today() + timedelta(days=2))
    res_room.room = room2
    reserv3.rooms.append(res_room)
    db.session.add(reserv3)
    db.session.commit()

    eq1 = Equipment('fen')
    eq2 = Equipment('fridge')
    eq3 = Equipment('tv')
    db.session.add_all([eq1, eq2, eq3])
    db.session.commit()

    room1.equipments.extend([eq2, eq3])
    room2.equipments.extend([eq1, eq3])
    db.session.add(room1)
    db.session.commit()

    print('Data inserted. Commit')
    db.session.close()