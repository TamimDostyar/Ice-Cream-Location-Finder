# makeadmin.py
from flask import Flask
from mapsource.db import db
from mapsource.loginP.models import User


def make_admin(app: Flask, username: str):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            user.is_admin = True
            db.session.commit()
            print(f"User {username} is now an admin.")
        else:
            print(f"User {username} not found.")
