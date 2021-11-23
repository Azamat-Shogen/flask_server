import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )

    def __init__(self, username: str, password: str, email=None):
        self.username = username
        self.password = password
        self.email = email

    def serialize(self):
        empty_list = []

        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'movies': empty_list,
            'created_at': self.created_at
        }


film_actors = db.Table(
    'film_actors',
    db.Column(
        'film_id', db.Integer,
        db.ForeignKey('films.id'),
        primary_key=True
    ),

    db.Column(
        'actor_id', db.Integer,
        db.ForeignKey('actors.id'),
        primary_key=True
    )
)

film_genres = db.Table(
    'film_genres',
    db.Column(
        'film_id', db.Integer,
        db.ForeignKey('films.id'),
        primary_key=True
    ),
    db.Column(
        'genre_id', db.Integer,
        db.ForeignKey('genres.id'),
        primary_key=True
    )
)


class Film(db.Model):
    __tablename__ = 'films'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.String(20), nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.00)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    actors = db.relationship(
        'Actor', secondary=film_actors,
        backref="film", cascade="all,delete")
    genre = db.relationship(
        'Genre', secondary=film_genres,
        backref="film", cascade="all,delete")

    def __init__(self, title: str, release_year: int, length: int, price=0.0, rating=None):
        self.title = title
        self.release_year = release_year
        self.length = length
        self.price = price
        self.rating = rating

    def serialize(self):
        actors_list = []
        for actor in self.actors:
            actors_list.append({"id": actor.id, "first_name": actor.first_name, "last_name": actor.last_name})

        genre_list = [{"id": g.id, "genre": g.genre} for g in self.genre]

        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year,
            'length': self.length,
            'price': self.price,
            'rating': self.rating,
            'date_added': self.date_added.isoformat(),
            'actors': actors_list,
            "genre": genre_list
        }


class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    films = db.relationship('Film', secondary=film_actors, backref="actor", cascade="all,delete")

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def serialize(self):
        empty_list = []
        for film in self.films:
            empty_list.append({"title": film.title, "id": film.id})
        return {
            'id': self.id,
            "first name": self.first_name,
            "last name": self.last_name,
            "movies": empty_list
        }


class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    genre = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, genre):
        self.genre = genre

    def serialize(self):
        return {
            'id': self.id,
            "genre": self.genre
        }

















