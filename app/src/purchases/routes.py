from flask import (Blueprint, request, jsonify)
from uuid import uuid1
from . import model
from flask import current_app
from users import model as userModel
from products import model as prodModels

bp = Blueprint('purchases',__name__, url_prefix='/purchases')

@bp.route('/<user_id>') #default: GET
def get_purchases(user_id):
    try:
        # traer lista de purchases de la base de datos
        purchases = model.get_db(user_id)
        return jsonify(purchases), 200 # ok
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Internal server error"}, 500

@bp.route('/<user_id>/<id>')
def get_purchase(user_id,id):
    try:
        # devolver el user segun id
        purchase = model.find_db(user_id,id)
        # errores si no existe
        if (purchase == None):
            return {"message": "Compra no encontrada"}, 404 # not found
        return purchase , 200 # ok 
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Internal server error"}, 500

@bp.route('/<user_id>', methods=['POST'])
def create_purchase(user_id):
    try:
        user = userModel.find_db(user_id)
        if (user == None):
            return {"message": "Usuario no encontrado"}, 404 # not found
        items = request.get_json()
        purchaseOut = model.save_db(user,items)
        return jsonify(purchaseOut), 201 # created
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Internal server error"}, 500
