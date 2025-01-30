from faker import Faker
from model import db, User, Venue, Event, Ticket
from app import app 
from datetime import datetime

fake=Faker()

with app.app_context():
    db.drop_all()
    db.create_all()
    for _ in range(10):
        user=User(name=fake.name(),email=fake.email(),phone=fake.phone_number())
        db.session.add(user)
        db.session.commit()
        venue=Venue(name=fake.name(),location=fake.address(),capacity=fake.random_int(min=100,max=1000))
        db.session.add(venue)
        db.session.commit()
        event=Event(title=fake.name(),date=fake.date(),time=fake.time(),venueid=venue.id,userid=user.id,ticketprice=fake.random_int(min=100,max=1000),description=fake.text())
        db.session.add(event)
        db.session.commit()
        ticket=Ticket(eventid=event.id,userid=user.id,ticketType='VIP',price=fake.random_int(min=100,max=1000))
        db.session.add(ticket)
        db.session.commit()
    print('Database seeded')
