# Démineur
Démineur (Démineur sur pygame)
💣 Minesweeper (Démineur) - Pygame

Un clone du célèbre jeu Démineur, développé en Python avec Pygame, basé sur la programmation orientée objet et la récursivité.

🎮 Description

Le but du jeu est de découvrir toutes les cases d'une grille sans tomber sur une mine.

Chaque case peut :

💥 Contenir une mine → défaite immédiate
🔢 Indiquer le nombre de mines adjacentes
⬜ Être vide → déclenche une révélation en chaîne (récursivité)

La première case cliquée est toujours sans mine.

🧠 Fonctionnalités
Génération aléatoire des mines
Système de grille dynamique
Révélation récursive des cases vides
Clic gauche : révéler une case
Clic droit :
🚩 Drapeau
❓ Point d’interrogation
Timer intégré ⏱️
Bouton de reset 🔄
Plusieurs niveaux de difficulté
Interface graphique avec Pygame
🗂️ Structure du projet
.
├── main.py              # Point d'entrée du jeu
├── Jeu.py               # Logique principale du jeu
├── Grille.py           # Gestion de la grille
├── Case.py             # Représentation d'une case
├── Timer.py            # Gestion du temps
├── fenetre.py          # Gestion de la fenêtre Pygame
├── dessin.py           # Fonctions de dessin
├── theme.py            # Couleurs / styles
│
├── *_renderer.py       # Rendu UI (grille, menu, entête, etc.)
├── bouton_reset.py     # Bouton reset
├── bouton_bonus.py     # (optionnel)
│
└── wtf.mp3             # Son (effet audio)
⚙️ Installation
1. Cloner le projet
git clone https://github.com/WillLaPlateforme/Demineur.git
cd minesweeper-pygame
2. Installer les dépendances
pip install pygame
▶️ Lancer le jeu
python main.py
🎯 Règles du jeu
Clique gauche → révéler une case
Clique droit → poser un drapeau / ?
Trouve toutes les cases sans mine pour gagner
Clique sur une mine → perdu
🧩 Concepts utilisés
Programmation orientée objet (POO)
Récursivité (révélation des cases vides)
Gestion d’événements avec Pygame
Séparation logique / affichage (renderer)
🚀 Améliorations possibles
Sauvegarde des scores
Classement des meilleurs temps
Animations
Mode multijoueur
Interface plus moderne
📚 Contexte du projet

Projet pédagogique visant à :

Développer une interface graphique
Manipuler des structures de données (grille)
Comprendre la récursivité
Structurer un projet Python proprement
