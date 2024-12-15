from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from .iceCreamTypes.models import IceCream
from .loginP.models import Favorit_store, db  

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

@bp.route("/remove-favorite/<int:shop_id>/<int:user_id>/", methods=["GET"])
@login_required
def remove_favorite(shop_id, user_id):
    if user_id != current_user.id:
        return "Error: Unauthorized", 403

    favorite_shop = Favorit_store.query.filter_by(id=shop_id, user_id=user_id).first()
    if favorite_shop:
        db.session.delete(favorite_shop)
        db.session.commit()
        return redirect(url_for('maps.maps_view'))
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
