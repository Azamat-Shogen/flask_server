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
        # film = Film.query.get_or_404(film_id)
        # actor = Actor.query.get_or_404(actor_id)
        #
        # if not film or not actor:
        #     return custom_error("shit", 400)

        stmt = sqlalchemy.insert(film_actors).values(film_id=film_id, actor_id=actor_id)
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return custom_error("Something went wrong", 422)

# TODO: DELETE
# TODO: UPDATE
