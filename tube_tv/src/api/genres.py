import sqlalchemy
from flask import Blueprint, json, jsonify, abort, request, make_response
from ..models import User, Film, Genre, db
from flask import Blueprint

bp = Blueprint('genres', __name__, url_prefix='/genres')


def custom_error(message, status_code):
    return make_response(jsonify(message), status_code)


@bp.route('', methods=['GET'])
def get_genres():
    genres = Genre.query.all()
    result = [g.serialize() for g in genres]
    return jsonify(result)


@bp.route('', methods=['POST'])
def add_genre():
    genres = Genre.query.all()
    mapped = list(map(lambda g: g.genre.lower(), genres))
    if 'genre' not in request.json:
        return custom_error("genre is required", 400)
    if request.json['genre'].lower() in mapped:
        return custom_error("existing genre, cant have duplicates", 400)

    try:
        g = Genre(genre=request.json['genre'])
        db.session.add(g)
        db.session.commit()
        return jsonify(g.serialize())
    except:
        return custom_error("Something went wrong", 422)


@bp.route('/<int:genre_id>', methods=['GET'])
def get_genre(genre_id: int):
    try:
        g = Genre.query.get_or_404(genre_id)
        return jsonify(g.serialize())
    except:
        return custom_error("something went wrong", 404)


@bp.route('/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id: int):
    try:
        g = Genre.query.get_or_404(genre_id)
        db.session.delete(g)
        db.session.commit()
        return jsonify({"message": "genre deleted successfully"})
    except:
        return custom_error("Failed to delete!", 404)


@bp.route('/<int:genre_id>', methods=['PUT', 'PATCH'])
def update_genre(genre_id):
    genres = Genre.query.all()
    g = Genre.query.get_or_404(genre_id)
    mapped = list(map(lambda x: x.genre.lower(), genres))

    if 'genre' not in request.json:
        print("*************")
        return custom_error("genre required", 400)
    if request.json['genre'].lower() in mapped:
        return custom_error("genre already exists", 400)

    try:
        g.genre = request.json['genre']
        db.session.commit()
        return jsonify({"message": "genre updated successfully"})
    except:
        return custom_error("something went wrong", 404)














