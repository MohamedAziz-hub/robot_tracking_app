# app.py
from flask import Flask, render_template, g
import sqlite3
import json
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
DATABASE = "database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/historique")
def historique():
    cur = get_db().cursor()
    cur.execute("SELECT id, date, duree_sec, nb_sorties_home FROM trajets ORDER BY id DESC")
    trajets = cur.fetchall()
    return render_template("historique.html", trajets=trajets)

@app.route("/trajet/<int:trajet_id>")
def trajet(trajet_id):
    cur = get_db().cursor()
    cur.execute("SELECT chemin, heure_debut, heure_fin FROM trajets WHERE id=?", (trajet_id,))
    row = cur.fetchone()
    if not row:
        return "Trajet non trouvé", 404

    chemin = json.loads(row[0])
    x = [p["x"] for p in chemin]
    y = [p["y"] for p in chemin]

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, '-o', label='Trajet')
    plt.title(f"Trajet {trajet_id} - {row[1]} → {row[2]}")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid(True)
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return render_template("trajet.html", plot_url=plot_url, id=trajet_id, debut=row[1], fin=row[2])

# 🔥 Démarrage du serveur
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)