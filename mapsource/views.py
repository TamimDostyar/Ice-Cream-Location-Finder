from flask import render_template, Blueprint, url_for

bp = Blueprint(
    "viewsc",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/",
)


@bp.route("/")
def greetings():
    return render_template("home.html")


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/maps")
def maps():
    return render_template("maps.html")
