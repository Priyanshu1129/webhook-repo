from flask import Flask
from app.extensions import init_app 
from flask_cors import CORS  
from app.webhook.routes import webhook


# Creating our flask app
def create_app():
    app = Flask(__name__)

    # cors configuration
    CORS(app)

    # Initialize MongoDB connection
    init_app(app)
    
    # registering all the blueprints
    app.register_blueprint(webhook)
    
    return app
