"""
BoutonNiveau : bouton de selection d'un niveau de difficulte dans le menu.
Une classe = un fichier (principe de responsabilite unique).
"""
import pygame
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_centre


class BoutonNiveau:
    """
    Bouton representant un niveau de difficulte (Facile / Moyen / Difficile).
    Change de couleur selon qu'il est actif, survole ou inactif.
    """

    def __init__(self, nom: str, rect: pygame.Rect, font: pygame.font.Font):
        self.nom   = nom
        self.rect  = rect
        self._font = font

    def dessiner(self, surface: pygame.Surface, actif: bool, survol: bool):
        """Dessine le bouton avec la couleur correspondant a son etat."""
        if actif:
            couleur = T.COULEUR_MENU_ACTIF
        elif survol:
            couleur = (55, 85, 140)
        else:
            couleur = T.COULEUR_MENU_INACTIF
        rect_arrondi(surface, couleur, self.rect, rayon=6)
        texte_centre(surface, self._font, self.nom.upper(), T.COULEUR_BONUS_TEXTE, self.rect)

    def collide(self, pos) -> bool:
        """Retourne True si la position donnee est dans le bouton."""
        return self.rect.collidepoint(pos)
