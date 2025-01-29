from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db=SQLAlchemy()


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    phone=db.Column(db.String(120), unique=True, nullable=False)

    tickets=db.relationship('Ticket',backref='user',lazy=True)



class Ticket(db.Model):
    __tablename__='tickets'
    id=db.Column(db.Integer, primary_key=True)
    eventid=db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    userid=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ticketType=db.Column(db.String(120), unique=True, nullable=False)
    price=db.Column(db.Float, nullable=False)
    status=db.Column(db.String(120), nullable=False,default='Available')


class Venue(db.Model):
    __tablename__='venues'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=True, nullable=False)
    location=db.Column(db.String(120), unique=True, nullable=False)
    capacity=db.Column(db.Integer, nullable=False)
    events=db.relationship('Event',backref='venue',lazy=True)

class Event(db.Model):
    __tablename__='events'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(80), unique=True, nullable=False)
    date=db.Column(db.String(120), unique=True, nullable=False)
    time=db.Column(db.String(120), nullable=False)
    venueid=db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    userid=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ticketprice=db.Column(db.Float, nullable=False)
    description=db.Column(db.String(120), nullable=False)
    tickets=db.relationship('Ticket',backref='event',lazy=True)




    
    def __repr__(self):
        return '<User %r>' % self.username