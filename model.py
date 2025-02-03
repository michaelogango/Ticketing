from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_migrate import Migrate



db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)

    tickets = db.relationship('Ticket', backref='user', lazy=True)

    serialize_rules = ('-tickets.user',) 


class Ticket(db.Model, SerializerMixin):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    eventid = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ticketType = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(120), nullable=False, default='Available')

    serialize_rules = ('-event.tickets', '-user.tickets')  


class Venue(db.Model, SerializerMixin):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(120), unique=False, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    events = db.relationship('Event', backref='venue', cascade='all, delete-orphan')



class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    date = db.Column(db.String(120), unique=False, nullable=False)
    time = db.Column(db.String(120), nullable=False)
    venueid = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ticketprice = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)

    tickets = db.relationship('Ticket', backref='event', cascade='all, delete-orphan')

    serialize_rules = ('-tickets.event', '-venue.events')

    def __repr__(self):
        return f'<Event {self.title}>'
