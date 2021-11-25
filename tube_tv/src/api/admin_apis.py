import sqlalchemy
from flask import jsonify, request, make_response
from ..models import Film, Genre, User, db, film_actors, film_genres, purchases
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


# TODO: POST
@bp.route('film-setup-genre/<int:film_id>', methods=['POST'])
def add_genre_to_film(film_id: int):
    if "genre_id" not in request.json:
        return custom_error("genre_id is required", 400)

    genre_id = request.json['genre_id']
    film = Film.query.get_or_404(film_id)
    genre = Genre.query.get_or_404(genre_id)

    try:
        stmt = sqlalchemy.insert(film_genres).values(film_id=film_id, genre_id=genre_id)
        db.session.execute(stmt)
        db.session.commit()
        return jsonify(True)
    except:
        return custom_error("Something went wrong", 422)


# TODO: DELETE
@bp.route('film-setup-genre/<int:film_id>', methods=['DELETE'])
def delete_film_genre(film_id: int):
    if "genre_id" not in request.json:
        return custom_error("genre_id is required", 400)

    genre_id = request.json['genre_id']
    film = Film.query.get_or_404(film_id)
    genre = Genre.query.get_or_404(genre_id)

    try:
        stmt = sqlalchemy.delete(film_genres).where(film_genres.c.film_id == film_id) \
            .where(film_genres.c.genre_id == genre_id)

        db.session.execute(stmt)
        db.session.commit()
        return jsonify({"message": "genre deleted from film"})
    except:
        return custom_error("Something went wrong", 422)


# TODO: Get all purchases
@bp.route('users/purchases', methods=['GET'])
def get_all_purchases():
    try:
        stmt = db.session.query(purchases)
        result = list(db.session.execute(stmt))
        purchases_list = [{"user_id": p.user_id, "film_id": p.film_id, "purchase_date": p.purchase_date} for p in
                          result]
        return jsonify(purchases_list)
    except:
        return jsonify({"Something went wrong"}, 422)


@bp.route('users/purchases', methods=['DELETE'])
def delete_purchase():
    if 'user_id' not in request.json or 'film_id' not in request.json:
        return custom_error("user_id and film_id required", 400)

    try:
        user_id = request.json['user_id']
        film_id = request.json['film_id']

        user = User.query.get_or_404(user_id)
        film = Film.query.get_or_404(film_id)

        stmt = sqlalchemy.delete(purchases).where(purchases.c.user_id == user_id) \
            .where(purchases.c.film_id == film_id)
        db.session.execute(stmt)
        db.session.commit()
        return jsonify({"message": "purchase removed from table"})
    except:
        return custom_error("Something went wrong", 422)
