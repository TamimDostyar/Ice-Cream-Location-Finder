import os
from dotenv import load_dotenv
load_dotenv() 

from mapsource import app

if __name__ == "__main__":
    app.run(debug=True, port=8000)
