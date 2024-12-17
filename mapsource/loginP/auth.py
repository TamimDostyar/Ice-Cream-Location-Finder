from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
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
        is_admin = data["is_admin"].lower() == "true"

        new_user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_password,
            is_admin=is_admin,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful.", "success")
        return redirect(url_for("viewsc.admin_welcome"))
    return render_template("signup.html")


@auth_bp.route("/createAccount", methods=["GET", "POST"], endpoint="createAccount")
def createAccount():
    if request.method == "POST":
        data = request.form
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            flash("An account with this email already exists. Please log in.", "error")
            return redirect(url_for("auth.register"))

        hashed_password = generate_password_hash(
            data["password"], method="pbkdf2:sha256"
        )
        is_admin = data["is_admin"].lower() == "true"

        new_user = User(
            username=data["username"],
            email=data["email"],
            password=hashed_password,
            is_admin=is_admin,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful.", "success")
        return redirect(url_for("viewsc.admin_welcome"))
    return render_template("add_account.html")


@auth_bp.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "POST":
        data = request.form
        user = User.query.filter_by(username=data["username"]).first()
        if user and check_password_hash(user.password, data["password"]):
            login_user(user)
            account_type = data.get("account_type")
            if account_type == "admin" and user.is_admin:
                return redirect(url_for("viewsc.admin_welcome"))
            elif account_type == "user" and not user.is_admin:
                return redirect(url_for("viewsc.maps_view"))
            else:
                flash("Invalid account type selected for this user.", "error")
                return redirect(url_for("auth.login"))
        flash("Login failed. Please check your username and password.", "error")
    return render_template("login.html")


@auth_bp.route("/logout", methods=["GET"], endpoint="logout")
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
    "/reset_password/<token>", methods=["GET", "POST"], endpoint="reset_password_token"
)
def reset_password(token):
    return render_template("reset_password.html")


@auth_bp.route("/manage_accounts", methods=["GET"], endpoint="manage_accounts")
@login_required
def manage_accounts():
    users = User.query.all()
    return render_template("manage_accounts.html", users=users)


@auth_bp.route(
    "/edit_user/<int:user_id>", methods=["GET", "POST"], endpoint="edit_user"
)
@auth_bp.route(
    "/edit_user/<int:user_id>", methods=["GET", "POST"], endpoint="edit_user"
)
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.username = request.form["username"]
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


@auth_bp.route(
    "/reset_password_user/<int:user_id>",
    methods=["POST"],
    endpoint="reset_password_user",
)
@auth_bp.route(
    "/reset_password_user/<int:user_id>",
    methods=["GET", "POST"],
    endpoint="reset_password_user",
)
@auth_bp.route(
    "/reset_password_user/<int:user_id>",
    methods=["POST"],
    endpoint="reset_password_user",
)
@login_required
def reset_password_user(user_id):
    user = User.query.get_or_404(user_id)
    new_password = request.form.get("new_password")
    if new_password:
        hashed_password = generate_password_hash(new_password, method="pbkdf2:sha256")
        user.password = hashed_password
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)



@auth_bp.route("/delete_user/<int:user_id>", methods=["POST"], endpoint="delete_user")
@login_required
def delete_user(user_id):
    if request.form.get('_method') == 'DELETE':
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully.", "success")
        return redirect(url_for("auth.manage_accounts"))
    return jsonify(success=False), 405



@auth_bp.route("/toggle_admin_status/<int:user_id>", methods=["POST"], endpoint="toggle_admin_status")
@login_required
def toggle_admin_status(user_id):
    user = User.query.get_or_404(user_id)
    is_admin = request.form["is_admin"].lower() == "true"  # Convert string to boolean
    user.is_admin = is_admin  # Update the user's admin status
    db.session.commit()  # Commit the change to the database
    return jsonify(success=True)  # Return a JSON response indicating success

