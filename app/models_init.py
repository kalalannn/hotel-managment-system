from models import engine, Base, Session, User, Hotel, Role, Feedback, Status, Reservation, Payment, Room, RoomCategory, Equipment
from datetime import datetime

# to delete all tables in db
# DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;

# creates all tables
Base.metadata.create_all(engine)
# creates new Session object using the configuration we’ve given the factory class
session = Session()

role1 = Role('admin')
role2 = Role('manager')
role3 = Role('user')
session.add(role1)
session.add(role2)
session.add(role3)
session.commit()

user1 = User('vasia007', '7juj', 'Vasia', 'Pupkin', 'vas_pup@mail.ru', datetime.today(), role2)
user2 = User('kloun', 'asdfasdf', 'Klounito', 'Shapito', 'kla@lol', datetime.today(), role3)
user3 = User('kalalannn', 'chapka*taschit', 'Nikolaj', 'Vorobiev', 'nik_vorob@gmail.com', datetime.today(), role1)
session.add(user1)
session.add(user2)
session.add(user3)
session.commit()

hotel1 = Hotel('Veveri', 'Hezky hotel', 4, 'vever. bityska 4', user1)
hotel2 = Hotel('Zamek', 'pekny vikend', 3, 'brno namesti republiky 8', user3)
hotel3 = Hotel('International', 'what the fuck', 5, 'minsk prospekt 34', user1)
session.add(hotel1)
session.add(hotel2)
session.add(hotel3)
session.commit()

status1 = Status('created')
status2 = Status('booked')
status3 = Status('canceled')
session.add(status1)
session.add(status2)
session.add(status3)
session.commit()

payment1 = Payment(21.44, 30.5, 4.08)
payment2 = Payment(5.4, 10.5, 1.22)
payment3 = Payment(18.8, 19.3, 1.08)
session.add(payment1)
session.add(payment2)
session.add(payment3)
session.commit()

reserv1 = Reservation(status1, user1, user3, payment1)
reserv2 = Reservation(status2, user1, user2, payment1)
reserv3 = Reservation(status3, user2, user3, payment2)
session.add(reserv1)
session.add(reserv2)
session.add(reserv3)
session.commit()


roomcat1 = RoomCategory('lux', 110, hotel1)
roomcat2 = RoomCategory('delux', 130, hotel1)
roomcat3 = RoomCategory('business', 90, hotel2)
roomcat4 = RoomCategory('normal', 50, hotel2)
roomcat5 = RoomCategory('poor', 30, hotel2)
session.add(roomcat1)
session.add(roomcat2)
session.add(roomcat3)
session.add(roomcat4)
session.add(roomcat5)
session.commit()

room1 = Room(2, roomcat2)
room2 = Room(3, roomcat2)
room3 = Room(4, roomcat3)
room4 = Room(4, roomcat4)
room5 = Room(5, roomcat5)
room6 = Room(6, roomcat5)
session.add(room1)
session.add(room2)
session.add(room3)
session.add(room4)
session.add(room5)
session.add(room6)
session.commit()

session.close()

# session.query(User).first()
# session.query(Hotel).filter_by(name='International').first()
# session.query(Role).filter_by(name='admin').first()