from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
import os
import models
from flask_jwt_extended import JWTManager

from db import db
from resources.cart import blp as CartBlueprint
from resources.product import blp as ProductBlueprint
from resources.user import blp as UserBlueprint
from resources.category import blp as CategoryBlueprint



def create_app(db_url=None):
    app = Flask(__name__)
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
    
    app.config["JWT_SECRET_KEY"] = "jose"
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(CartBlueprint)
    api.register_blueprint( ProductBlueprint)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CategoryBlueprint)

    return app