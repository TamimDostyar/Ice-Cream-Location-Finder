import os
from dotenv import load_dotenv

from mapsource import app, db


load_dotenv()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
