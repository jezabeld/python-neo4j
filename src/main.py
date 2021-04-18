from flask import Flask
from users import routes as userRoutes

app = Flask(__name__)
app.url_map_strict_slashes = False

@app.route('/')
def hello_world():
    return {
        'message':'Willcommen!'
    }, 200

app.register_blueprint(userRoutes.bp)