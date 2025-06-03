import os
from flask_pymongo import PyMongo

mongo = PyMongo()

def init_app(app):
    app.config["MONGO_URI"] = os.getenv("MONGODB_URI")
    mongo.init_app(app)
    app.extensions['pymongo'] = mongo  
    print("[MongoDB] Connected successfully!")
