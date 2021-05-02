from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model
from flask import current_app
from users import model as userModel
from products import model as prodModels
from errors import ProductNotFound, UserNotFound, PurchaseNotFound, MissingParameter

bp = Blueprint('purchases',__name__, url_prefix='/purchases')

@bp.route('/<user_id>') #default: GET
def get_purchases(user_id):
    user = userModel.find_db(user_id)
    if (user == None):
        raise UserNotFound(user_id)
    
    purchases = model.get_db(user_id)

    return jsonify(purchases), 200 

@bp.route('/<user_id>/<id>')
def get_purchase(user_id,id):
    user = userModel.find_db(user_id)
    if (user == None):
        raise UserNotFound(user_id)

    purchase = model.find_db(user_id,id)
    if (purchase == None):
        raise PurchaseNotFound(id)

    return purchase , 200  


@bp.route('/<user_id>', methods=['POST'])
def create_purchase(user_id):
    user = userModel.find_db(user_id)
    if (user == None):
        raise UserNotFound(user_id)

    items = request.get_json()
    products = []
    for item in items:
        product = prodModels.find_db(item['id'])
        if (product == None):
            raise ProductNotFound(item['id'])
        products.append({**product, 'quantity': item['quantity']})

    purchaseOut = model.save_db(user,products)
    return jsonify(purchaseOut), 201 

