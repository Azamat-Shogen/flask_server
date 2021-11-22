import sqlalchemy
from flask import Blueprint, json, jsonify, abort, request, make_response
from ..models import User, Film, Genre, db, film_actors, Actor
from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')


def custom_error(message, status_code):
    return make_response(jsonify(message), status_code)


# TODO: POST
@bp.route('film-setup-actors', methods=['POST'])
def add_actor_to_film():
    if "film_id" not in request.json:
        return custom_error("film_id is required", 400)
    if "actor_id" not in request.json:
        return custom_error("actor_id is required", 400)

    film_id = request.json['film_id']
    actor_id = request.json['actor_id']

    try:
        stmt = sqlalchemy.insert(film_actors).values(film_id=film_id, actor_id=actor_id)
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return custom_error("Something went wrong", 422)


# TODO: DELETE
@bp.route('film-setup-actors/<int:film_id>', methods=['DELETE'])
def delete_film_actor(film_id: int):
    if 'actor_id' not in request.json:
        return custom_error("actor is required", 400)

    try:
        actor_id = request.json['actor_id']
        stmt = sqlalchemy.delete(film_actors).where(film_actors.c.film_id == film_id) \
            .where(film_actors.c.actor_id == actor_id)
        db.session.execute(stmt)
        db.session.commit()
        return jsonify({"message": "actor removed from film"})
    except:
        return custom_error("something went wrong", 422)

