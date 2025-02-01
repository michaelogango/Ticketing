from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model import db, User, Ticket, Event, Venue
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket.db'

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app)
CORS(app)  # Allowing all origins by default

class Home(Resource):
    def get(self):
        return {"message": "Welcome to the Ticketing System"}, 200

api.add_resource(Home, '/')


# User Routes
class UserResource(Resource):
    def get(self):
        return make_response(jsonify([user.to_dict() for user in User.query.all()]), 200)

    def post(self):
        data = request.get_json()
        user = User(name=data['name'], email=data['email'], phone=data['phone'])
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "User created successfully",
            **user.to_dict()
        }), 201

api.add_resource(UserResource, '/users')


class UserById(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return make_response(jsonify(user.to_dict()), 200)

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        data = request.json
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        db.session.commit()
        return jsonify({"message": "User updated successfully!"})

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully!"})

api.add_resource(UserById, '/users/<int:user_id>')


# Ticket Routes
class TicketResource(Resource):
    def get(self):
        return jsonify([
            {
                "id": ticket.id,
                "eventid": ticket.eventid,
                "userid": ticket.userid,
                "ticketType": ticket.ticketType,
                "price": ticket.price,
                "status": ticket.status
            } for ticket in Ticket.query.all()
        ])

    def post(self):
        data = request.get_json()
        ticket = Ticket(
            eventid=data['eventid'],
            userid=data['userid'],
            ticketType=data['ticketType'],
            price=data['price'],
            status='Sold'
        )
        db.session.add(ticket)
        db.session.commit()
        return jsonify({
            "message": "Ticket created successfully",
            "id": ticket.id
        }), 201

api.add_resource(TicketResource, '/tickets')


class TicketById(Resource):
    def get(self, ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404
        return make_response(jsonify(ticket.to_dict()), 200)

    def delete(self, ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({"message": "Ticket deleted successfully!"})

api.add_resource(TicketById, '/tickets/<int:ticket_id>')


# Event Routes
class EventResource(Resource):
    def get(self):
        return jsonify([
            {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "date": event.date,
                "time": event.time,
                "venueid": event.venueid,
                "userid": event.userid,
                "ticketprice": event.ticketprice
            } for event in Event.query.all()
        ])

    def post(self):
        data = request.get_json()
        event = Event(
            title=data['title'],
            date=data['date'],
            time=data['time'],
            venueid=data['venueid'],
            userid=data['userid'],
            ticketprice=data['ticketprice'],
            description=data['description']
        )
        db.session.add(event)
        db.session.commit()
        return jsonify({"message": "Event created successfully", "id": event.id}), 201

api.add_resource(EventResource, '/events')


class EventById(Resource):
    def get(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return make_response(jsonify(event.to_dict()), 200)

    def delete(self, event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully!"})

api.add_resource(EventById, '/events/<int:event_id>')


# Venue Routes
class VenueResource(Resource):
    def get(self):
        return jsonify([
            {
                "id": venue.id,
                "name": venue.name,
                "location": venue.location,
                "capacity": venue.capacity
            } for venue in Venue.query.all()
        ])

    def post(self):
        data = request.get_json()
        venue = Venue(
            name=data['name'],
            location=data['location'],
            capacity=data['capacity']
        )
        db.session.add(venue)
        db.session.commit()
        return jsonify({"message": "Venue created successfully", "id": venue.id}), 201

api.add_resource(VenueResource, '/venues')


class VenueById(Resource):
    def get(self, venue_id):
        venue = Venue.query.get(venue_id)
        if not venue:
            return jsonify({"error": "Venue not found"}), 404
        return make_response(jsonify({
            "id": venue.id,
            "name": venue.name,
            "location": venue.location,
            "capacity": venue.capacity
        }), 200)

    def delete(self, venue_id):
        venue = Venue.query.get(venue_id)
        if not venue:
            return jsonify({"error": "Venue not found"}), 404
        db.session.delete(venue)
        db.session.commit()
        return jsonify({"message": "Venue deleted successfully!"})

api.add_resource(VenueById, '/venues/<int:venue_id>')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
