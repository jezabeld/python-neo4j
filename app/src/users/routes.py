from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model
from flask import current_app
from errors import ProductNotFound, UserNotFound, MissingParameter

bp = Blueprint('users',__name__, url_prefix='/users')

@bp.route('/') #default: GET
def get_users():
    usuarios = model.get_db()
    
    return jsonify(usuarios), 200 

@bp.route('/<id>')
def get_user(id):
    user = model.find_db(id)
    if (user == None):
        raise UserNotFound(id)
    
    return user

@bp.route('/', methods=['POST'])
def create_user():
    user = request.get_json()
    userOut = model.save_db(user)

    return jsonify(userOut), 201 


@bp.route('/', methods=['PUT'])
def update_user():
    user = request.get_json()
    if ( not 'id' in user):
        raise MissingParameter('id')

    userOut = model.update_db(user)
    if (userOut == None):
        raise UserNotFound(user['id'])

    return jsonify(userOut), 200 


@bp.route('/<id>', methods=['DELETE'])
def delete_user(id):
    user = model.delete_db(id)
    if (user == None):
        raise UserNotFound(id)

    return jsonify(user), 200 
