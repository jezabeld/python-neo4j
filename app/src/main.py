from flask import Flask, current_app
from users import routes as userRoutes
from products import routes as productRoutes
from purchases import routes as purchaseRoutes
from werkzeug.exceptions import HTTPException
import traceback

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def ping():
    return {
        'message':'Willcommen! Service is working.'
    }, 200

app.register_blueprint(userRoutes.bp)
app.register_blueprint(productRoutes.bp)
app.register_blueprint(purchaseRoutes.bp)

@app.errorhandler(Exception)
def handle_exception(e):
    current_app.logger.error(e)
    traceback.print_tb(e.__traceback__)

    # pass through HTTP errors
    if isinstance(e, HTTPException):
        current_app.logger.error(e)
        return {
            'type': e.name if not hasattr(e,'type') else e.name,
            'message': e.description
        }, e.code

    # non HTTP errors
    return {"message": "Internal server error"}, 500
