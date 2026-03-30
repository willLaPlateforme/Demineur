"""
Minesweeper - Point d'entree
La Plateforme | POO + Pygame
Logique : Case.py + Grille.py + Jeu.py
Graphique : graphique/
"""
from graphique.fenetre import Fenetre


def main():
    app = Fenetre()
    app.lancer()


if __name__ == "__main__":
    main()
