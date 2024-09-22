from flask import Flask
from . import views
from flask_bootstrap import Bootstrap
import time
from datetime import timedelta

app = Flask(__name__)
Bootstrap(app)
app.config.from_mapping(SECRET_KEY="source_code")

# Register the blueprint
app.register_blueprint(views.bp)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)
