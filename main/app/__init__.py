from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import Config

mongo = PyMongo()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)

    from app.views.home import home_bp
    from app.views.data import data_bp
    from app.views.create import create_bp
    from app.views.update import update_bp
    from app.views.delete import delete_bp
    from app.views.auth import auth_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(create_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(auth_bp)

    return app
