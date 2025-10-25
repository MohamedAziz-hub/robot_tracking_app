# ros_listener.py
#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
import sqlite3
import json
from datetime import datetime

# Configuration
HOME_X, HOME_Y = 0.0, 0.0  # À remplacer par la vraie position "home"
MIN_POINTS_FOR_TRAJET = 5  # Nombre minimum de points pour valider un trajet

class TrajetTracker:
    def __init__(self):
        self.trajet_en_cours = []
        self.sorti_de_home = False
        self.start_time = None
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS trajets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                heure_debut TEXT,
                heure_fin TEXT,
                duree_sec INTEGER,
                chemin TEXT,
                nb_sorties_home INTEGER DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()

    def odom_callback(self, data):
        x = data.pose.pose.position.x
        y = data.pose.pose.position.y
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        distance_to_home = ((x - HOME_X)**2 + (y - HOME_Y)**2)**0.5
        est_a_home = distance_to_home < 0.5

        if not est_a_home and not self.sorti_de_home:
            self.sorti_de_home = True
            self.start_time = now
            self.trajet_en_cours = []

        if self.sorti_de_home:
            self.trajet_en_cours.append({"x": x, "y": y})

        # Si retour à home et trajet en cours → sauvegarde
        if est_a_home and self.sorti_de_home and len(self.trajet_en_cours) >= MIN_POINTS_FOR_TRAJET:
            self.sauvegarder_trajet(self.start_time, now, self.trajet_en_cours)
            self.sorti_de_home = False
            self.trajet_en_cours = []

    def sauvegarder_trajet(self, debut, fin, points):
        duree = len(points)  # En nombre de points
        chemin_json = json.dumps(points)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO trajets (date, heure_debut, heure_fin, duree_sec, chemin, nb_sorties_home)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            debut.split()[0],
            debut,
            fin,
            duree,
            chemin_json,
            1
        ))
        conn.commit()
        conn.close()
        print(f"✅ Trajet sauvegardé : {debut} → {fin}")

if __name__ == '__main__':
    rospy.init_node('ros_listener')
    tracker = TrajetTracker()
    rospy.Subscriber('/odom', Odometry, tracker.odom_callback)
    rospy.spin()