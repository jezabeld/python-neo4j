from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model

bp = Blueprint('users',__name__, url_prefix='/users')

@bp.route('/') #default: GET
def get_users():
    # traer lista de usuario de la base de datos
    usuarios = model.get_db()
    return jsonify(usuarios), 200 # ok

@bp.route('/<id>')
def get_user(id):
    # devolver el user segun id
    user = model.find_db(id)
    # errores si no existe
    if (user == None):
        return {"message": "Usuario no encontrado"}, 404 # not found
    return user , 200 # ok 

@bp.route('/', methods=['POST'])
def post_user():
    user = request.get_json()
    # chequear que el user tiene toda la data necesaria (?)
    # guardar el user en la db o devolver error
    userid = model.save_db(user)
    return userid, 201 # created

@bp.route('/', methods=['PUT'])
def put_user():
    user = request.get_json()
    # chequear que el user tiene toda la data necesaria
    if ( not 'id' in user):
        return {"message": "Se requiere el id"}, 400 # bad request
    # modificar el user en la db o devolver error
    user = model.update_db(user)
    if (user == None):
        return {"message": "Usuario no encontrado"}, 404 # not found
    return user, 200 # ok + contenido

@bp.route('/<id>', methods=['DELETE'])
def delete_user(id):
    # borrar el user en la db o devolver error
    user = model.delete_db(id)
    if (user == None):
        return {"message": "Usuario no encontrado"}, 404 # not found
    return user, 200 # ok + contenido