from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model
from flask import current_app

bp = Blueprint('products',__name__, url_prefix='/products')

@bp.route('/') #default: GET
def get_products():
    author = request.args.get('author')
    category = request.args.get('category')
    try:
        # traer lista de products de la base de datos
        productos = model.get_db(author,category)
        return jsonify(productos), 200 # ok
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Internal server error"}, 500

@bp.route('/<id>')
def get_product(id):
    try:
        # devolver el user segun id
        user = model.find_db(id)
        # errores si no existe
        if (user == None):
            return {"message": "Producto no encontrado"}, 404 # not found
        return user , 200 # ok 
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Internal server error"}, 500

@bp.route('/', methods=['POST'])
def create_product():
    try:
        product = request.get_json()
        # chequear que el product tiene toda la data necesaria (?)
        # guardar el product en la db o devolver error
        productOut = model.save_db(product)
        return jsonify(productOut), 201 # created
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Internal server error"}, 500

@bp.route('/', methods=['PUT'])
def update_product():
    try:
        product = request.get_json()
        # chequear que el product tiene toda la data necesaria
        if ( not 'id' in product):
            return {"message": "Se requiere el id"}, 400 # bad request
        # modificar el product en la db o devolver error
        product = model.update_db(product)
        if (product == None):
            return {"message": "Producto no encontrado"}, 404 # not found
        return jsonify(product), 200 # ok + contenido
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Internal server error"}, 500

@bp.route('/<id>', methods=['DELETE'])
def delete_product(id):
    try:
        # borrar el product en la db o devolver error
        product = model.delete_db(id)
        if (product == None):
            return {"message": "Producto no encontrado"}, 404 # not found
        return jsonify(product), 200 # ok + contenido
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Internal server error"}, 500