"""
Project Name: Jeopardy Python Game
Project Author(s): 
    Joseph Lefkovitz (github.com/lefkovitz),
    Santiago Rached Alvarez (https://github.com/Tw0S41nt)
Last Modified: 7/29/2025

File Purpose: Web application backend logic.
"""

# Standard library imports.
import os

# Third-party imports.
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Import board.
from utils import get_random_game_board

# Local application imports.

# Create the application.
app = Flask(__name__)
load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Configure the database.
db = SQLAlchemy()
db.init_app(app)

@app.route("/")
def homepage():
    """ Display the application homepage. """
    try:
        game_board = get_random_game_board('jeopardy.tsv')

        return f"<pre>{game_board}</pre>"
    
    except FileNotFoundError:
        return "Jeopardy.tsv not found."
    except Exception as e:
        return f"An error occurred: {e}", 500
