from flask import Flask
import os
from routes.coach import coach_bp
from routes.client import client_bp


# Import the setup_database function from createBaseData
from data.setup_db import setup_database

app = Flask(__name__)

app.register_blueprint(coach_bp)
app.register_blueprint(client_bp)

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    # Ensure the database is set up before Sstarting the app
    setup_database()
    app.run(debug=True)
