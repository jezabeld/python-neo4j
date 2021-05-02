from flask import Flask
from users import routes as userRoutes
from products import routes as productRoutes
from purchases import routes as purchaseRoutes

app = Flask(__name__)
app.url_map_strict_slashes = False

@app.route('/')
def hello_world():
    return {
        'message':'Willcommen!'
    }, 200

app.register_blueprint(userRoutes.bp)
app.register_blueprint(productRoutes.bp)
app.register_blueprint(purchaseRoutes.bp)