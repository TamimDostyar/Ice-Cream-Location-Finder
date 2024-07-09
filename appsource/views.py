from flask import render_template, Flask

app = Flask(__name__)


@app.route("/inbox")
def greetings():
    return render_template("views.html")
