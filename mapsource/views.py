from flask import render_template, Blueprint, url_for

bp = Blueprint(
    "viewsc",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/",  # or any other prefix you intend to use
)


@bp.route("/")
def greetings():
    return render_template("home.html")


@bp.route("/about")
def about():
    return render_template("about.html")
