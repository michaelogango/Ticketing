from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    tickets = db.relationship('Ticket', backref='user', lazy=True)

    serialize_rules = ('-tickets.user',)  # Prevent circular serialization

    # Password setter (hashes password)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Password checker
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Convert object to dictionary for JSON response
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }  # Prevent circular serialization


class Ticket(db.Model, SerializerMixin):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    eventid = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ticketType = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(120), nullable=False, default='Available')

    serialize_rules = ('-event.tickets', '-user.tickets')  # Prevent circular references


class Venue(db.Model, SerializerMixin):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(120), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    events = db.relationship('Event', backref='venue', lazy=True)

    serialize_rules = ('-events.venue',)  # Avoid nesting too deep


class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    date = db.Column(db.String(120), unique=True, nullable=False)
    time = db.Column(db.String(120), nullable=False)
    venueid = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ticketprice = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120), nullable=False)

    tickets = db.relationship('Ticket', backref='event', lazy=True)

    serialize_rules = ('-tickets.event', '-venue.events')

    def __repr__(self):
        return f'<Event {self.title}>'
