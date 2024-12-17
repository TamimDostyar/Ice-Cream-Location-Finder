from flask import Blueprint, redirect, url_for, render_template,Flask, request, jsonify
from flask_login import login_required, current_user
from .iceCreamTypes.models import IceCream
from .loginP.models import Favorit_store, User, db
from collections import defaultdict

bp = Blueprint(
    "viewsc",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/",
)
main_bp = Blueprint("main", __name__)


@bp.route("/", methods=["GET"])
def greetings():
    return render_template("home.html")


@bp.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@bp.route("/explore", methods=["GET"], endpoint="explore")
def explore():
    icecreams = IceCream.query.all()
    return render_template("explore.html", icecreams=icecreams)


@bp.route("/maps", methods=["GET"], endpoint="maps_view")
@login_required
def maps_view():
    return render_template("maps.html", current_user=current_user)

@bp.route("/favorite/", methods=["GET"])
@login_required
def favorite_view():
    user_id = current_user.id
    favorites = Favorit_store.query.filter_by(user_id=user_id).all()
    return render_template("favorite.html", favorites=favorites)

@bp.route('/add_favorite', methods=['POST'])
def add_favorite():
    data = request.json
    user_id = current_user.id

    existing_favorite = Favorit_store.query.filter_by(
        title=data['title'],
        user_id=user_id
    ).first()

    if existing_favorite:
        return jsonify({'message': 'This shop is already in your favorites!'}), 400

    favorite = Favorit_store(
        title=data['title'],
        location=data['location'],
        url=data['url'],
        rating=data['rating'],
        user_id=user_id
    )
    db.session.add(favorite)
    db.session.commit()

    return jsonify({'message': 'Favorite added successfully!'}), 200

@bp.route("/remove-favorite/<int:shop_id>/<int:user_id>/", methods=["GET"])
@login_required
def remove_favorite(shop_id, user_id):
    if user_id != current_user.id:
        return "Error: Unauthorized", 403

    favorite_shop = Favorit_store.query.filter_by(id=shop_id, user_id=user_id).first()
    if favorite_shop:
        db.session.delete(favorite_shop)
        db.session.commit()
        return redirect(url_for('viewsc.favorite_view'))
    else:
        return "Error: Shop not found or not a favorite of the user", 404


@bp.route("/edit_web", methods=["GET"], endpoint="edit_web")
@login_required
def edit_web():
    icecreams = IceCream.query.all()
    return render_template("edit_web.html", current_user=current_user, icecreams=icecreams)



@bp.route("/continue_as_user", methods=["GET"], endpoint="continue_as_user")
@login_required
def continue_as_user():
    return render_template("continue_as_user.html", current_user=current_user)


@bp.route("/admin_welcome", methods=["GET"], endpoint="admin_welcome")
@login_required
def admin_welcome():
    return render_template("admin_welcome.html", current_user=current_user)

@bp.route('/favorites')
def list_favorite_stores():
    results = db.session.query(
        Favorit_store.title,
        Favorit_store.location,
        Favorit_store.url,
        Favorit_store.rating,
        User.username,
        User.email
    ).join(User, Favorit_store.user_id == User.id).all()

    stores_with_users = {}

    for title, location, url, rating, username, email in results:
        store_key = (title, location, rating)

        if store_key not in stores_with_users:
            stores_with_users[store_key] = {
                "title": title,
                "location": location,
                "url": url,
                "rating": rating,
                "users": []
            }

        stores_with_users[store_key]['users'].append({
            "username": username,
            "email": email
        })

    grouped_stores = list(stores_with_users.values())
    return render_template('listoffavorites.html', stores=grouped_stores)

