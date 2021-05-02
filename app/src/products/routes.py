from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model
from flask import current_app
from errors import ProductNotFound, UserNotFound, MissingParameter

bp = Blueprint('products',__name__, url_prefix='/products')

@bp.route('/') #default: GET
def get_products():
    author = request.args.get('author')
    category = request.args.get('category')
    productos = model.get_db(author,category)

    return jsonify(productos), 200 

@bp.route('/<id>')
def get_product(id):
    product = model.find_db(id)
    if (product == None):
        raise ProductNotFound(id)

    return product , 200 

@bp.route('/', methods=['POST'])
def create_product():
    product = request.get_json()
    productOut = model.save_db(product)
    
    return jsonify(productOut), 201 

@bp.route('/', methods=['PUT'])
def update_product():
    product = request.get_json()
    if ( not 'id' in product):
        raise MissingParameter('id')

    productOut = model.update_db(product)
    if (productOut == None):
        raise ProductNotFound(product['id'])
    
    return jsonify(product), 200 

@bp.route('/<id>', methods=['DELETE'])
def delete_product(id):
    product = model.delete_db(id)
    if (product == None):
        raise ProductNotFound(id)
    
    return jsonify(product), 200 
