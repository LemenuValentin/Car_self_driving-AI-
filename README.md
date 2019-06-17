# Intelligence artificielle pour une voiture autonome

1) Contexte
Ce dépôt présente le design et le développement d'une intelligence artificielle (IA) capable de conduire une voiture dans un environnement simplifié, c'est-à-dire dans un environnement ne contenant ni piétons, ni croisement de route. L'objectif est uniquement de pouvoir faire rouler une voiture sur la route.

2) Installation du simulateur
Il est nécessaire de télécharger le simulateur de conduite. Pour ce faire, référez-vous au guide d'installation suivant : https://github.com/udacity/self-driving-car-sim

Ce simulateur permet :
- D'une part, d'enregistrer des données d'apprentissage sur l'un des deux circuits disponibles (training phase).
- D'autre part, de lancer la simulation pour tester le modèle d'intelligence artificiel élaboré (test phase).

3) Démarrer la simulation 
Afin de démarer la simulation, il faut tout d'abord lancer le simulateur de conduite d'udacity et aller en mode autonome. Une fois la voiture sur le circuit prête à démarrer, lancer le code drive.py et la simulation commence.

4) Description des fichiers et répertoires
Ce dépot contient 3 fichiers ainsi que 2 dossiers : 
- Fichier Features.py --> Ce script permet de calculer les features (distance droite et gauche) et de créer un fichier CSV reprennant ces features associées à l'angle de volant de la voiture correspondant.
- Fichier Linear_regression_model.py --> Ce script permet de créer le modèle de régression linéaire en utilisant le fichier CSV précédemment créé avec Features.py
- Fichier drive.py --> Ce script permet de lancer la simulation en utilisant le modèle créé avec Linear_regression_model.py

5) Algorithmes et bibliothèques utilisées
Préprocessing : Utilisation de la bibliotèque openCV afin de réaliser le traitement d'image nécessaire pour le calcul des distances gauches et droites.
Modèle : Utilisation de la librairie scikit learn (sk-learn) afin de réaliser la régression linéaire. Pickle est également utilisé afin de sauvegarder et charger le modèle.
Lancement simulation : Utilisation de socketio et eventlet pour communicquer avec le simulateur udacity. 
Autre : Utilisation de Numpy, CSV et panda pour diverses opérations.
