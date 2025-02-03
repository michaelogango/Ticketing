from app import app, db
from model import User, Venue, Event, Ticket
from faker import Faker
import random

fake = Faker()

# Create users, venues, events, and tickets
with app.app_context():
    db.drop_all()  # Drop all existing tables
    db.create_all()  # Create all tables from models

    # Generate 10 users with unique names, emails, and phones, respecting length constraints
    for _ in range(10):
        user = User(
            name=fake.name()[:80],  # Ensure name is max 80 characters
            email=fake.email()[:120],  # Ensure email is max 120 characters
            phone=fake.phone_number()[:10]  # Ensure phone is exactly 10 characters
        )
        db.session.add(user)
    db.session.commit()

    # Generate 5 venues with unique names and locations
    for _ in range(5):
        venue = Venue(
            name=fake.company()[:80],  # Ensure venue name is max 80 characters
            location=fake.address()[:120],  # Ensure location is max 120 characters
            capacity=random.randint(100, 1000)
        )
        db.session.add(venue)
    db.session.commit()

    # Generate 10 events with valid venue and user associations, respecting length constraints
    venue_ids = [v.id for v in Venue.query.all()]
    user_ids = [u.id for u in User.query.all()]

    for _ in range(10):
        event = Event(
            title=fake.bs()[:80],  # Ensure title is max 80 characters
            date=fake.date_this_year().strftime('%Y-%m-%d')[:120],  # Ensure date is max 120 characters
            time=fake.time()[:120],  # Ensure time is max 120 characters
            venueid=random.choice(venue_ids),
            userid=random.choice(user_ids),
            ticketprice=random.randint(100, 1000),
            description=fake.text(max_nb_chars=120)  # Ensure description is max 120 characters
        )
        db.session.add(event)
    db.session.commit()

    # Generate 30 tickets with valid user and event associations, respecting length constraints
    event_ids = [e.id for e in Event.query.all()]
    user_ids = [u.id for u in User.query.all()]

    for _ in range(30):
        ticket = Ticket(
            eventid=random.choice(event_ids),
            userid=random.choice(user_ids),
            ticketType='VIP'[:120],  # Ensure ticket type is max 120 characters
            price=random.randint(100, 1000),
            status=random.choice(['Available', 'Sold', 'Reserved'])[:120]  # Ensure status is max 120 characters
        )
        db.session.add(ticket)
    db.session.commit()

    print('Database seeded successfully!')
