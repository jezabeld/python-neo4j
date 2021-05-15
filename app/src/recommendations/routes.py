from flask import (Blueprint, request, jsonify)
from . import model
from flask import current_app
from errors import ProductNotFound, UserNotFound, MissingParameter

bp = Blueprint('recommendations',__name__, url_prefix='/recommendations')

@bp.route('/by_category/<category>')
def get_product_by_category(category):
    """ Category best sellers """
    products = model.find_by_category(category)
    
    return jsonify(products) , 200 

@bp.route('/related_product/<id>')
def get_related_product(id):
    """ Users also bought """
    products = model.find_related_product(id)
    
    return jsonify(products) , 200 