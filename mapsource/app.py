from flask import Flask
import views

bp = views.bp

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(bp)
