import hashlib
from logging import error
import secrets
import requests
import sqlalchemy
from flask import Blueprint, jsonify, abort, request, make_response
from ..models import User, db
from flask import Blueprint

bp = Blueprint('users', __name__, url_prefix='/users')


def custom_error(message, status_code):
    return make_response(jsonify(message), status_code)


def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()


@bp.route('', methods=['GET'])  # decorator takes path and lst of HTTP verbs
def get_users():
    users = User.query.all()  # ORM performs SELECT query
    result = []
    for user in users:
        result.append(user.serialize())
    return jsonify(result)


@bp.route('', methods=['POST'])
def create_user():
    users = User.query.all()
    if 'username' not in request.json or 'password' not in request.json:
        return custom_error("username and password required", 400)

    if len(request.json['username']) < 3:
        return custom_error("your username is too short", 400)

    if len(request.json['password']) < 6:
        return custom_error("password should be at least 6 characters long", 400)

    user_names = list(map(lambda u: u.username, users))
    if request.json['username'] in user_names:
        return custom_error("Username already exists", 400)

    if 'email' in request.json:
        if len(request.json['email']) < 5 or '@' not in request.json['email']:
            return custom_error("should be a valid email", 400)
        users_emails = list(map(lambda u: u.email, users))

        if request.json['email'] in users_emails:
            return custom_error("email already exists", 400)

    try:
        user = User(
            username=request.json['username'],
            password=scramble(request.json['password']),
            email=request.json['email'] if 'email' in request.json else None

        )
        db.session.add(user)  # prepare CREATE statement
        db.session.commit()  # execute CREATE statement
        return jsonify(user.serialize())
    except error:
        return make_response('something went wrong', 404)


@bp.route('/<int:id>', methods=['GET'])
def get_user(id: int):
    try:
        user = User.query.get_or_404(id)
        return jsonify(user.serialize())
    except:
        return make_response('user doesnt exist', 404)


@bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': "user deleted successfully"})
    except:
        return make_response('failed to delete the user', 404)


@bp.route('/<int:id>', methods=['PUT', 'PATCH'])
def update_user(id: int):
    try:
        users = User.query.all()
        user = User.query.get_or_404(id)
        if not ('username' in request.json or 'password' in request.json or 'email' in request.json):
            return make_response('missing attributes: [username, password, email]', 404)

        if 'username' in request.json:
            if len(request.json['username']) < 3:
                return make_response('username is too short', 400)

            user_names = list(map(lambda u: u.username, users))
            if request.json['username'] in user_names:
                return make_response("Username already exists", 400)

            user.username = request.json['username']

        if 'password' in request.json:
            if len(request.json['password']) < 8:
                return make_response('password is too short', 400)
            user.password = scramble(request.json['password'])

        if 'email' in request.json:
            if len(request.json['email']) < 5 or '@' not in request.json['email']:
                return make_response("should be a valid email", 400)
            users_emails = list(map(lambda u: u.email, users))

            if request.json['email'] in users_emails:
                return make_response("email already exists", 400)

            user.email = request.json['email']

        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
