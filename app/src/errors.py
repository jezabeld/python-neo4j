from werkzeug.exceptions import HTTPException

class ProductNotFound(HTTPException):
    def __init__(self, product_id):
        self.code = 404
        self.type = "ProductNotFound"
        self.description = f"Product {product_id} not found"

class UserNotFound(HTTPException):
    def __init__(self, user_id):
        self.code = 404
        self.type = "UserNotFound"
        self.description = f"User {user_id} not found"

class PurchaseNotFound(HTTPException):
    def __init__(self, purchase_id):
        self.code = 404
        self.type = "PurchaseNotFound"
        self.description = f"Purchase {purchase_id} not found"

class MissingParameter(HTTPException):
    def __init__(self, parameter_name):
        self.code = 400
        self.type = "MissingParameter"
        self.description = f"Parameter '{parameter_name}' not found"