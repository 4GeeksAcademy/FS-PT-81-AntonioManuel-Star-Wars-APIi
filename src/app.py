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
from models import db, Users, Characters, Planets, Favourite_Planet, Favourite_Character
from flask_migrate import Migrate
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# Metodo GET #

@app.route('/characters', methods=['GET'])
def handle_characters():
    characters = Characters.query.all()
    print(characters)
    # characters = [characters.serialize() for characters in characters]
    # return jsonify({"msg": "OK", "data": "characters" }), 200
    return jsonify([character.serialize() for character in characters])

@app.route('/character/<int:character_id>', methods=['GET'])
def handle_character_id(character_id):
    character = Characters.query.get(character_id)
    print(character)
    if character:
        return jsonify(character.serialize()), 200
    # return jsonify({"msg": "character with id" + str(id), "character": character.serialize()}), 200

@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = Planets.query.all()
    print(planets)
    planets = [planet.serialize() for planet in planets]
    return jsonify(planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def handle_planet_id(planet_id):
    planet = Planets.query.get(planet_id)
    print(planet)
    if planet:
        return jsonify(planet.serialize()), 200
    # return jsonify({"msg": "planet with id" + str(id), "planet": planet.serialize()}), 200

@app.route('/users', methods=['GET'])
def handle_users():
    users = Users.query.all()
    print(users)
    users = [user.serialize() for user in users]
    return jsonify(users), 200

@app.route('/users/favourites', methods=['GET'])
def handle_users_fav():
    user_id = 1
    favourite_character = Favourite_Character.query.filter_by(user_id = user_id).all()
    favourite_planets = Favourite_Planet.query.filter_by(user_id = user_id).all()

    favourites = {
        'characters':[fav.serialize() for fav in favourite_character],
        'planets': [fav.serialize() for fav in favourite_planets]
    }
    return jsonify(favourites), 200
# Me falta metodo get de fav de users

# Metodo POST #

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def handle_fav_planet(planet_id):
    user_id = 1

    existing_favourites = Favourite_Planet.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if existing_favourites:
        return jsonify({'error': 'planet already in favourites'}), 400
    

    new_favourite_planet = Favourite_Planet(user_id = user_id, planet_id = planet_id)
    db.session.add(new_favourite_planet)
    db.session.commit()

    return jsonify({"msg": "Planet added to favourites"})

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def handle_fav_character(character_id):
    user_id = 1

    existing_favourites = Favourite_Character.query.filter_by(user_id = user_id, character_id = character_id).first()
    if existing_favourites:
        return jsonify({'error': 'character already in favourite'}, 400)
    new_favourite_character = Favourite_Character(user_id = user_id, character_id = character_id)
    db.session.add(new_favourite_character)
    db.session.commit()

    return jsonify({'msg': 'Character added to favourites'})

# Delete #

@app.route('/favourite/planet/<int:planet_id>', methods=['DELETE'])
def handle_delete_planet(planet_id):
    user_id = 1

    favourite = Favourite_Planet.query.filter_by(user_id = user_id, planet_id = planet_id).first()
    if not favourite:
        return jsonify({'error': 'favourites planets not found'}), 400
    
    db.session.delete(favourite)
    db.session.commit()

    return jsonify({'msg': 'favourite planet delete'}), 200

@app.route('/favourite/character/<int:character_id>', methods=['DELETE'])
def handle_delete_character(character_id):
    user_id = 1

    favourite = Favourite_Character.query.filter_by(user_id = user_id, character_id = character_id).first()
    if not favourite:
        return jsonify({'error': 'favourites characters not found'}), 400
    
    db.session.delete(favourite)
    db.session.commit()

    return jsonify({'msg': 'favourite character delete'}), 200




    




  





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
