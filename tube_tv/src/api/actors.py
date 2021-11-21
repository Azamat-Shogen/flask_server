import sqlalchemy
from flask import Blueprint, json, jsonify, abort, request, make_response
from ..models import User, Film, Actor, db
from flask import Blueprint

bp = Blueprint('actors', __name__, url_prefix='/actors')


def custom_error(message, status_code):
    return make_response(jsonify(message), status_code)


@bp.route('', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    result = [actor.serialize() for actor in actors]
    return jsonify(result)


@bp.route('', methods=['POST'])
def add_actor():
    actors = Actor.query.all()
    if 'first_name' not in request.json:
        return custom_error("first name required", 400)
    if 'last_name' not in request.json:
        return custom_error('last name required', 400)

    filtered = list(filter
                    (lambda x: x.first_name.lower() == request.json['first_name'].lower()
                    and x.last_name.lower() == request.json['last_name'].lower(), actors))
    if len(filtered) > 0:
        return custom_error("Actor already exists", 400)

    try:
        actor = Actor(
            first_name=request.json['first_name'],
            last_name=request.json['last_name']
        )
        db.session.add(actor)
        db.session.commit()
        return jsonify(actor.serialize())
    except:
        return custom_error("Failed to add")
