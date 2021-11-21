import hashlib
from logging import error
import secrets
import requests
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
        db.session.add(film) # prepare CREATE statement
        db.session.commit() # execute CREATE statement
        return jsonify(film.serialize())
    except:
        # print('******* ', error)
        return custom_error('something went wrong', 404)
