import sqlalchemy
from flask import Blueprint, json, jsonify, abort, request, make_response
from ..models import User, Film, db
from flask import Blueprint

bp = Blueprint('films', __name__, url_prefix='/films')


def custom_error(message, status_code):
    return make_response(jsonify(message), status_code)


@bp.route('', methods=['GET'])
def get_films():
    films = Film.query.all()
    result = []
    for film in films:
        result.append(film.serialize())
    return jsonify(result)


@bp.route('', methods=['POST'])
def add_film():
    if 'title' not in request.json or 'release_year' not in request.json or 'length' not in request.json:
        return custom_error('attributes are missing', 400)

    try:
        film = Film(
            title=request.json['title'],
            release_year=request.json['release_year'],
            length=request.json['release_year'],
            price=request.json['price'] if 'price' in request.json else 0.0,
            rating=request.json['rating'] if 'rating' in request.json else None
        )
        db.session.add(film)  # prepare CREATE statement
        db.session.commit()  # execute CREATE statement
        return jsonify(film.serialize())
    except:
        # print('******* ', error)
        return custom_error('something went wrong', 404)


@bp.route('/<int:film_id>', methods=['GET'])
def get_film(film_id: int):
    try:
        film = Film.query.get_or_404(film_id)
        return jsonify(film.serialize())
    except:
        return custom_error("Something went wrong", 404)


@bp.route('/<int:film_id>', methods=['DELETE'])
def delete_film(film_id: int):
    try:
        film = Film.query.get_or_404(film_id)
        db.session.delete(film)
        db.session.commit()
        return jsonify({"message": "film deleted successfully"})
    except:
        return custom_error("Failed to delete", 404)


@bp.route('/<int:film_id>', methods=['PUT', 'PATCH'])
def update_film(film_id: int):

    for el in request.json:
        if el not in ["title", "release_year", "length", "price", "rating"]:
            return custom_error("no matching attributes passed", 400)

    try:
        film = Film.query.get_or_404(film_id)
        if 'title' in request.json:
            film.title = request.json['title']
        if 'release_year' in request.json:
            film.release_year = request.json['release_year']
        if 'length' in request.json:
            film.length = request.json['length']
        if 'price' in request.json:
            film.price = request.json['price']
        if 'rating' in request.json:
            film.rating = request.json['rating']

        db.session.commit()
        return jsonify({"message": "successfully updated"})

    except:
        return custom_error("Was not able to update the film", 404)













