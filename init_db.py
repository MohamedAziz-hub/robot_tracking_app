# init_db.py
import sqlite3

DATABASE = "database.db"

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS trajets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        heure_debut TEXT NOT NULL,
        heure_fin TEXT NOT NULL,
        duree_sec INTEGER NOT NULL,
        chemin TEXT NOT NULL,
        nb_sorties_home INTEGER DEFAULT 1
    )
''')

conn.commit()
conn.close()
print("✅ Base de données créée : database.db")