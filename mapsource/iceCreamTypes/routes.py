# routes.py in iceCreamTypes
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .models import IceCream, db  # Ensure correct import
from flask_login import login_required

ice_cream_bp = Blueprint("ice_cream_bp", __name__)


@ice_cream_bp.route("/add_icecream", methods=["POST"])
def add_icecream():
    data = request.get_json()
    new_icecream = IceCream(
        name=data["name"],
        description=data["description"],
        url=data["url"],
        price=data["price"],
    )
    db.session.add(new_icecream)
    db.session.commit()
    return jsonify({"message": "Ice cream added successfully"}), 201


@ice_cream_bp.route("/icecreams", methods=["GET"])
def get_icecreams():
    icecreams = IceCream.query.all()
    icecream_list = [
        {
            "name": icecream.name,
            "description": icecream.description,
            "url": icecream.url,
            "price": icecream.price,
        }
        for icecream in icecreams
    ]
    return jsonify(icecream_list)


@ice_cream_bp.route("/admin", methods=["GET"])
@login_required
def admin_view():
    icecreams = IceCream.query.all()
    return render_template("admin.html", icecreams=icecreams, current_user=current_user)


@ice_cream_bp.route("/add_icecream_form", methods=["POST"])
@login_required
def add_icecream_form():
    name = request.form["name"]
    description = request.form["description"]
    url = request.form["url"]
    price = request.form["price"]
    new_icecream = IceCream(name=name, description=description, url=url, price=price)
    db.session.add(new_icecream)
    db.session.commit()
    return redirect(url_for("ice_cream_bp.admin_view"))
