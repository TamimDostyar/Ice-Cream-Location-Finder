# __init__.py
from flask import Flask
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from .db import db

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from .loginP import models
        from .iceCreamTypes.models import IceCream
        from .loginP.auth import auth_bp, login_manager

        login_manager.init_app(app)
        app.register_blueprint(auth_bp)

        from .routes import bp as main_bp

        app.register_blueprint(main_bp)

        from .iceCreamTypes.routes import ice_cream_bp

        app.register_blueprint(ice_cream_bp)

        db.create_all()

    return app


app = create_app()
from mapsource.makeadmin import make_admin

app = create_app()
make_admin(app, "tamimdostyar")
