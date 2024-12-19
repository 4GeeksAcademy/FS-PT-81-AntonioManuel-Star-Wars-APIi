from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(80), unique = False, nullable = False)
    is_active = db.Column(db.Boolean(), unique = False, nullable = False)

    def __repr__(self):
        return '<Users %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    age = db.Column(db.String(80),  nullable = False)
    gender = db.Column(db.String(80),  nullable = False)
    birth_year = db.Column(db.String(80),  nullable = False)
    eye_color = db.Column(db.String(80),  nullable = False)
    hair_color = db.Column(db.String(80),  nullable = False)
    skin_color = db.Column(db.String(80),  nullable = False)
    height = db.Column(db.Numeric,  nullable = False)
    mass = db.Column(db.Numeric , nullable = False)
    
    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "height": self.height,
            "mass": self.mass
            # do not serialize the password, its a security breach
        }
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), unique = True, nullable = False)
    climate = db.Column(db.String(80), nullable = False)
    diameter = db.Column(db.Numeric, nullable = False)
    orbital_period = db.Column(db.Numeric, nullable = False)
    gravity = db.Column(db.Numeric, nullable = False)
    population = db.Column(db.String(80), nullable = False)
    terrain = db.Column(db.String(80), nullable = False)
    surface_water = db.Column(db.Numeric, nullable = False)
    rotation_period = db.Column(db.Numeric, nullable = False)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "rotation_period": self.rotation_period

            # do not serialize the password, its a security breach
        }
class Favourite_Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
    characters = db.relationship(Characters)
    
    def __repr__(self):
        return '<FavCharacter %r>' % self.character_id

    def serialize(self):
        return {
            "id": self.id,
            "character_id": self.character_id,
            "user_id": self.user_id
        }
    
class Favourite_Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_id =db.Column(db.Integer, db.ForeignKey('planets.id'))
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
    planets = db.relationship(Planets)

    def __repr__(self):
        return '<FavPlanet %r>' % self.planet_id

    def serialize(self):
        return {
            "id": self.id,
            "planet_id": self.planet_id,
            "user_id": self.user_id
        }