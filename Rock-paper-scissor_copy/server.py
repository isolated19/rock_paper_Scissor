
from flask import Flask, request, redirect, url_for, render_template, g, jsonify
import sqlite3

app = Flask(__name__, static_folder='static', template_folder='templates')
DATABASE = "game.db"

# Function to connect to the database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Allows accessing columns by name
    return g.db

# Function to create the table if it doesn't exist
def create_table():
    db = sqlite3.connect(DATABASE)
    db.execute('''CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player1 TEXT NOT NULL,
                    player2 TEXT NOT NULL,
                    player1_score INTEGER DEFAULT 0,
                    player2_score INTEGER DEFAULT 0
                 )''')
    db.commit()
    db.close()

# Close database connection at the end of the request
@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Home page (player input form)
@app.route("/")
def index():
    return render_template("index.html")

# Save players to the database
@app.route("/save_players", methods=["POST"])
def save_players():
    player1 = request.form.get("player1", "").strip()
    player2 = request.form.get("player2", "").strip()

    if not player1 or not player2:
        return "Both player names are required!", 400

    db = get_db()
    db.execute("INSERT INTO scores (player1, player2) VALUES (?, ?)", (player1, player2))
    db.commit()

    return redirect(url_for("game"))

# Game page
@app.route("/game")
def game():
    db = get_db()
    cur = db.execute("SELECT player1, player2, player1_score, player2_score FROM scores ORDER BY id DESC LIMIT 1")
    players = cur.fetchone()

    if not players:
        return "No players found. Please start a new game.", 400

    return render_template("game1.html", 
                           player1=players["player1"], 
                           player2=players["player2"], 
                           player1_score=players["player1_score"], 
                           player2_score=players["player2_score"])

# # Route to save scores
# @app.route('/save_score', methods=['POST'])
# def save_score():
#     data = request.json
#     player1, score1 = data['player1'], data['score1']
#     player2, score2 = data['player2'], data['score2']

#     db = get_db()
#     # cur = db.cursor()
    
#     # Save scores into the database
#     db.execute("INSERT INTO scores (player_1, player1_score) VALUES (?, ?)", (player1, score1))
#     db.execute("INSERT INTO scores (player_2, player2_score) VALUES (?, ?)", (player2, score2))
    
#     db.commit()
#     db.close()

#     return jsonify({"message": "Scores saved successfully"})

# @app.route('/save_score', methods=['POST'])
# def save_score():
#     data = request.json
#     player1, score1 = data['player1'], data['score1']
#     player2, score2 = data['player2'], data['score2']

#     db = get_db()
    
#     # Update scores instead of inserting a new row
#     db.execute("""
#         UPDATE scores 
#         SET player1_score = ?, player2_score = ? 
#         WHERE player1 = ? AND player2 = ? 
#         ORDER BY id DESC LIMIT 1
#     """, (score1, score2, player1, player2))

#     db.commit()
#     return jsonify({"message": "Scores updated successfully"})


@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.json
    player1, score1 = data['player1'], data['score1']
    player2, score2 = data['player2'], data['score2']

    db = get_db()

    # Find the latest game entry
    cur = db.execute("""
        SELECT id FROM scores
        WHERE player1 = ? AND player2 = ?
        ORDER BY id DESC LIMIT 1
    """, (player1, player2))

    latest_game = cur.fetchone()

    if latest_game:
        game_id = latest_game["id"]
        db.execute("""
            UPDATE scores 
            SET player1_score = ?, player2_score = ? 
            WHERE id = ?
        """, (score1, score2, game_id))
        db.commit()
        return jsonify({"message": "Scores updated successfully"})

    return jsonify({"error": "No matching game found"}), 400



# Leaderboard page
@app.route("/leaderboard")
def leaderboard():
    db = get_db()
    cur = db.execute("""
        SELECT player1, player1_score, player2, player2_score 
        FROM scores 
        ORDER BY (player1_score + player2_score) DESC 
        LIMIT 10
    """)
    scores = cur.fetchall()
    
    return render_template("leaderboard.html", scores=scores)

# Debugging route to check database entries
@app.route("/show_players")
def show_players():
    db = get_db()
    players = db.execute("SELECT * FROM scores ORDER BY id DESC LIMIT 5").fetchall()
    return jsonify([dict(row) for row in players])

if __name__ == "__main__":
    create_table()  # Ensure the table exists before starting the app
    app.run(debug=True)
