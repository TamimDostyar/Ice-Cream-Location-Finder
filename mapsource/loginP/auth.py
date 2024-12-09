from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from .. import db
from .models import User

auth_bp = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route("/register", methods=["GET", "POST"], endpoint="register")
def register():
    if request.method == "POST":
        data = request.form
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            flash("An account with this email already exists. Please log in.", "error")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(
            data["password"], method="pbkdf2:sha256"
        )
        new_user = User(
            username=data["username"], email=data["email"], password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data["username"]).first()
        if user and check_password_hash(user.password, data["password"]):
            login_user(user)
            if user.username == "admin":
                return redirect(url_for("viewsc.admin_welcome"))
            return redirect(url_for("viewsc.maps_view"))
        flash("Login failed. Please check your username and password.", "error")
    return render_template("login.html")


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("viewsc.greetings"))


@auth_bp.route("/forgot_password", methods=["GET", "POST"], endpoint="forgot_password")
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            flash("A password reset link has been sent to your email.", "success")
        else:
            flash("No account found with that email address.", "error")
        return redirect(url_for("auth.forgot_password"))
    return render_template("forgot_password.html")


@auth_bp.route(
    "/reset_password/<token>", methods=["GET", "POST"], endpoint="reset_password"
)
def reset_password(token):
    return render_template("reset_password.html")
