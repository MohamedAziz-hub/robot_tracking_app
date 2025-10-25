# Robot Tracking App

## Description
Cette application web permet de suivre en temps réel un robot autonome.  
Elle affiche :
- La position actuelle du robot.
- Les cycles/trajectoires réalisés.
- L’historique des trajets sur une interface web interactive.

Le projet utilise :
- Flask pour le serveur web
- Matplotlib pour visualiser les trajectoires
- SQLite pour stocker les trajets
- ROS (Robot Operating System) pour récupérer les données de position du robot via le topic `/odom`

---

## Fonctionnalités
- Suivi en temps réel des positions du robot
- Visualisation graphique des trajets
- Historique des trajets avec date, durée et nombre de sorties de "home"
- Enregistrement automatique des trajets dans la base SQLite

---

## Structure du projet
