import os

from flask import Flask
from flask_smorest import Api

from db import db



from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

def create_app(db_url = None): #create_app --> flask automatically detaects the flas app by decalre like this 
    app = Flask(__name__)

    #app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db") #connection to db by passing url or by givinng that sqlite url
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "postgresql+psycopg2://f0f4bea271659f284ef04e0a0293fb5e6d8edb7c9ab1ddaec336cef7eb3d6272:sk_wE7Hu510UoJ8oc51oTSYt@db.prisma.io:5432/postgres?sslmode=require"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)# initialize the flask sqlalchemy extension n giving to the flask app so that we can connect flask app to sqlalchemy

    api = Api(app)

    import models
    with app.app_context(): # Create tables when the app starts
        db.create_all()


    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app

app = create_app()
