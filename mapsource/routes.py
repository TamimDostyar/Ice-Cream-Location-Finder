from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .iceCreamTypes.models import IceCream  # Import your models

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


@bp.route("/edit_web", methods=["GET"], endpoint="edit_web")
@login_required
def edit_web():
    return render_template("edit_web.html", current_user=current_user)


@bp.route("/continue_as_user", methods=["GET"], endpoint="continue_as_user")
@login_required
def continue_as_user():
    return render_template("continue_as_user.html", current_user=current_user)


@bp.route("/admin_welcome", methods=["GET"], endpoint="admin_welcome")
@login_required
def admin_welcome():
    return render_template("admin_welcome.html", current_user=current_user)
