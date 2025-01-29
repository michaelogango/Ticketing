from flask import Flask, jsonify, request,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model import db, User, Ticket,Event, Venue

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ticket.db'



db.init_app(app)
migrate=Migrate(app, db)

# @app.before_first_request
# def create_tables():
#     db.create_all()


####################### API ENDPOINTS (USERS) #######################
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method=='GET':
        return make_response([user.to_dict() for user in User.query.all()],200)

    elif request.method=='POST':
        data=request.get_json()
        user=User(name=data['name'], email=data['email'], phone=data['phone'])
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"user created Successfully", "id": user.id, "name": user.name, "email": user.email, "phone": user.phone}), 201




    # users=User.query.all()
    # return jsonify([{"id": user.id, "name": user.name, "email": user.email, "phone": user.phone} for user in users])

  
# @app.route('/users', methods=['POST'])
# def create_user():
#     data=request.get_json()
#     user=User(name=data['name'], email=data['email'], phone=data['phone'])
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({"message":"user created Successfully", "id": user.id, "name": user.name, "email": user.email, "phone": user.phone}), 201


@app.route('/users/<int:user_id>', methods=['PUT','DELETE','GET'])
def user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    else:
        if request.method=="GET":
            return make_response(user.to_dict(),200)

        elif request.method=="PUT":
            data = request.json
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.phone = data.get('phone', user.phone)
            user.user_type = data.get('user_type', user.user_type)
            db.session.commit()
            return jsonify({"message": "User updated successfully!"})

        elif request.method=="DELETE":
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully!"})
            





#     
# @app.route('/users/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return jsonify({"error": "User not found"}), 404
#     db.session.delete(user)
#     db.session.commit()
#     return jsonify({"message": "User deleted successfully!"})


####################### API ENDPOINTS (TICKETS) #######################
@app.route('/tickets', methods=['GET',"POST"])
def get_tickets():
    tickets=Ticket.query.all()
    return jsonify([{"id": ticket.id, "name": ticket.name, "description": ticket.description, "status": ticket.status} for ticket in tickets])

@app.route('/tickets', methods=['POST'])
def create_ticket():
    data=request.get_json()
    ticket=Ticket.query.filter_by(event_id=data['event_id'], status= 'Available'). first()
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    ticket.user_id=data['user_id']
    ticket.status='Sold'
    db.session.commit()
    return jsonify({"message":"ticket created Successfully", "id": ticket.id, "name": ticket.name, "description": ticket.description, "status": ticket.status}), 201

@app.route('/tickets/<int:ticket_id>', methods=['PUT','DELETE','GET'])
def update_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    data = request.json
    ticket.name = data.get('name', ticket.name)
    ticket.description = data.get('description', ticket.description)
    ticket.status = data.get('status', ticket.status)
    db.session.commit()
    return jsonify({"message": "Ticket updated successfully!"})

@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket deleted successfully!"})

####################### API ENDPOINTS (EVENT) #######################
@app.route('/events', methods=['GET',"POST"])
def get_events():
    events=Event.query.all()
    return jsonify([{"id": event.id, "name": event.name, "description": event.description, "date": event.date} for event in events])

@app.route('/events', methods=['POST'])
def create_event():
    data=request.get_json()
    event=Event(name=data['name'], description=data['description'], date=data['date'])
    db.session.add(event)
    db.session.commit()
    return jsonify({"message":"event created Successfully", "id": event.id, "name": event.name, "description": event.description, "date": event.date}), 201

@app.route('/events/<int:event_id>', methods=['PUT','DELETE','GET'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    data = request.json
    event.name = data.get('name', event.name)
    event.description = data.get('description', event.description)
    event.date = data.get('date', event.date)
    db.session.commit()
    return jsonify({"message": "Event updated successfully!"})

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted successfully!"})

####################### API ENDPOINTS (VENUE) #######################
@app.route('/venues', methods=['GET',"POST"])
def get_venues():
    venues=Venue.query.all()
    return jsonify([{"id": venue.id, "name": venue.name, "location": venue.location, "capacity": venue.capacity} for venue in venues])

@app.route('/venues', methods=['POST'])
def create_venue():
    data=request.get_json()
    venue=Venue(name=data['name'], location=data['location'], capacity=data['capacity'])
    db.session.add(venue)
    db.session.commit()
    return jsonify({"message":"venue created Successfully", "id": venue.id, "name": venue.name, "location": venue.location, "capacity": venue.capacity}), 201

@app.route('/venues/<int:venue_id>', methods=['PUT','DELETE','GET'])
def update_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return jsonify({"error": "Venue not found"}), 404
    data = request.json
    venue.name = data.get('name', venue.name)
    venue.location = data.get('location', venue.location)
    venue.capacity = data.get('capacity', venue.capacity)
    db.session.commit()
    return jsonify({"message": "Venue updated successfully!"})

@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if not venue:
        return jsonify({"error": "Venue not found"}), 404
    db.session.delete(venue)
    db.session.commit()
    return jsonify({"message": "Venue deleted successfully!"})




if __name__ == '__main__':
    app.run(debug=True, port=5000)