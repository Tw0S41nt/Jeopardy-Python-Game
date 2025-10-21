"""
Project Name: Jeopardy Python Game
Project Author(s): 
    Joseph Lefkovitz (github.com/lefkovitz),
    Santiago Rached Alvarez (https://github.com/Tw0S41nt)
Last Modified: 9/8/2025

File Purpose: Web application backend logic.
"""

# Standard library imports.
import os
import json

# Third-party imports.
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Import board.
from utils import get_random_game_board, get_host_code

# Local application imports.

# Create the application.
app = Flask(__name__)
load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Configure the database.
db = SQLAlchemy()
db.init_app(app)

# Create database schema.
class JeopardyGame(db.Model):
    """ Represent a single Jeopardy game. """
    game_id = db.Column(db.Integer, primary_key = True)
    r1 = db.Column(db.Integer, nullable=False)
    r2 = db.Column(db.Integer, nullable=False)
    final_jeopardy = db.Column(db.Integer, nullable=False)
    host_code = db.Column(db.Text, nullable=False)

class JeopardyBoard(db.Model):
    """ Represent one board of a single Jeopardy game. """
    id = db.Column(db.Integer, primary_key = True)
    board = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def homepage():
    """ Display the application homepage. """
    try:
        game_board = get_random_game_board('jeopardy.tsv')

        return render_template("index.html", board=game_board)

    except FileNotFoundError:
        return "Jeopardy.tsv not found."
    except Exception as e:
        return f"An error occurred: {e}", 500

def create_game_db_obj(round=0, number_categories = 6):
    """ Get JSON string of board object (list). """
    rounds = [[2, 3], [1, 3], [1, 2]]
    board = get_random_game_board(
        'jeopardy.tsv',
        disallowed_rounds = rounds[round],
        number_categories=number_categories
    )
    return json.dumps(board)

@app.route("/game/new/")
def game_new():
    """ Create a new game entry in the db. """
    try:
        # Create boards and game objects.
        r1 = create_game_db_obj()
        r1_db = JeopardyBoard(board=r1)

        r2 = create_game_db_obj(round=1)
        r2_db = JeopardyBoard(board=r2)

        final = create_game_db_obj(round=2, number_categories=1)
        final_db = JeopardyBoard(board=final)

        db.session.add(r1_db)
        db.session.add(r2_db)
        db.session.add(final_db)
        db.session.commit()

        new_game = JeopardyGame(
            r1=r1_db.id,
            r2=r2_db.id,
            final_jeopardy=final_db.id,
            host_code=get_host_code()
        )
        db.session.add(new_game)
        db.session.commit()
        return f"<pre>{r1}</pre><br><br><pre>{r2}</pre><br><br><pre>{final}</pre>"
    except FileNotFoundError:
        return "Jeopardy.tsv not found.", 500
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route("/game/<int:game_id>/<int:round>")
def game_view(game_id, round):
    """ Load the game round and return it from the database. """
    game = JeopardyGame.query.filter_by(game_id = game_id).first_or_404()
    r1 = JeopardyBoard.query.filter_by(id=game.r1).first_or_404()
    r2 = JeopardyBoard.query.filter_by(id=game.r2).first_or_404()
    final = JeopardyBoard.query.filter_by(id=game.final_jeopardy).first_or_404()
    rounds = [r1, r2, final]
    # Load the board corresponding to the round.
    board = json.loads(rounds[round].board)
    return str(board)

if __name__ == "__main__":
    app.run()
