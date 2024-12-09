from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)

    with app.app_context():
        # Import models within the app context
        from .loginP import models

        # Import blueprints within the app context
        from .loginP.auth import auth_bp, login_manager
        login_manager.init_app(app)
        app.register_blueprint(auth_bp)

        from .routes import bp as main_bp
        app.register_blueprint(main_bp)

        db.create_all()  # Ensure that the tables are created

    return app

app = create_app()
