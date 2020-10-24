from models import engine, Base, Session, User, Hotel, Role, Feedback, Status, Reservation, Payment, Room, RoomCategory, Equipment
from datetime import datetime

# to delete all tables in db
# DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;

# creates all tables
Base.metadata.create_all(engine)
# creates new Session object using the configuration we’ve given the factory class
session = Session()

# role1 = Role('admin')
# role2 = Role('manager')
# role3 = Role('user')

# user1 = User('vasia007', '7juj', 'Vasia', 'Pupkin', 'vas_pup@mail.ru', datetime.today(), role2)
# user2 = User('kloun', 'asdfasdf', 'Klounito', 'Shapito', 'kla@lol', datetime.today(), role3)
# user3 = User('kalalannn', 'chapka*taschit', 'Nikolaj', 'Vorobiev', 'nik_vorob@gmail.com', datetime.today(), role1)

# hotel1 = Hotel('Veveri', 'Hezky hotel', 4, 'vever. bityska 4', user1)
# hotel2 = Hotel('Zamek', 'pekny vikend', 3, 'brno namesti republiky 8', user3)
# hotel3 = Hotel('International', 'what the fuck', 5, 'minsk prospekt 34', user1)

# session.add(role1)
# session.add(role2)
# session.add(role3)

# session.add(user1)
# session.add(user2)
# session.add(user3)

# session.add(hotel1)
# session.add(hotel2)
# session.add(hotel3)

# session.commit()
# session.close()

# session.query(User).filter_by(username='vasia007').first()
# session.query(Hotel).filter_by(name='International').first()
# session.query(Role).filter_by(name='admin').first()