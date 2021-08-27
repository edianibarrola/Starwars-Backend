"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Person, Planet, Starship, Vehicle
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager





app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "KS&*$8sd"  # Change this!
jwt = JWTManager(app)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# --------------User Routes---------------
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(username=username).first()
    if user is None or password != user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/user', methods=['GET'])
# @jwt_required()
def get_all_users():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    response_body = {
        "msg": "Here are all of the users.",
        "users": all_users
    }
    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    user_info = User.query.get(id).serialize()
    
    response_body = {
        "msg": "Here is the selected user.",
        "User": user_info
    }
    return jsonify(user_info), 200

# --------------People Routes---------------

@app.route('/person', methods=['GET'])
def get_all_people():
    all_people = Person.query.all()
    all_people = list(map(lambda x: x.serialize(), all_people))
    response_body = {
        "msg": "Here are all of the People."
    }
    return jsonify(all_people), 200

@app.route('/person/<int:id>', methods=['GET'])
def get_one_person(id):
    person_info = Person.query.get(id).serialize()
    
    response_body = {
        "msg": "Here is the selected user.",
        "User": person_info
    }
    return jsonify(person_info), 200
# --------------Planet Routes---------------

@app.route('/planet', methods=['GET'])
def get_all_planets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    response_body = {
        "msg": "Here are all of the People."
    }
    return jsonify(all_planets), 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):
    planet_info = Planet.query.get(id).serialize()
    
    response_body = {
        "msg": "Here is the selected Planet.",
        "User": planet_info
    }
    return jsonify(planet_info), 200
# --------------Vehicle Routes---------------

@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    all_vehicles = Vehicle.query.all()
    all_vehicles = list(map(lambda x: x.serialize(), all_vehicles))
    response_body = {
        "msg": "Here are all of the vehicles."
    }
    return jsonify(all_vehicles), 200

@app.route('/vehicle/<int:id>', methods=['GET'])
def get_one_vehicle(id):
    vehicle_info = Vehicle.query.get(id).serialize()
    
    response_body = {
        "msg": "Here is the selected Vehicle.",
        "User": vehicle_info
    }
    return jsonify(vehicle_info), 200
# --------------Starship Routes---------------

@app.route('/starship', methods=['GET'])
def get_all_starships():
    all_starships = Starship.query.all()
    all_starships = list(map(lambda x: x.serialize(), all_starships))
    response_body = {
        "msg": "Here are all of the Starships."
    }
    return jsonify(all_starships), 200

@app.route('/starship/<int:id>', methods=['GET'])
def get_one_starship(id):
    starship_info = Starship.query.get(id).serialize()
    
    response_body = {
        "msg": "Here is the selected Starship.",
        "User": starship_info
    }
    return jsonify(starship_info), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
