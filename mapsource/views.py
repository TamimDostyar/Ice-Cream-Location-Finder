from flask import render_template, Blueprint

bp = Blueprint(
    "views",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/",
)


@bp.route("/inbox")
def greetings():
    return render_template("views.html")
