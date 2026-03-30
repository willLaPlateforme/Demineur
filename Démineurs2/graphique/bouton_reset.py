"""
BoutonReset : bouton RESET cliquable dans l'en-tete.
Une classe = un fichier (principe de responsabilite unique).
"""
import pygame
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_centre


class BoutonReset:
    """
    Bouton RESET dans la barre d'en-tete.
    Change de label et de couleur selon l'etat de la partie :
      - Partie en cours  -> "RESET"  (bleu)
      - Victoire         -> " WIN!"  (vert)
      - Defaite          -> " RIP!"  (rouge)
    """

    LARGEUR = 80
    HAUTEUR = 34

    def __init__(self, font: pygame.font.Font):
        self._font = font
        self.rect  = pygame.Rect(0, 0, self.LARGEUR, self.HAUTEUR)

    def centrer(self, cx: int, cy: int):
        """Centre le bouton sur le point (cx, cy)."""
        self.rect.center = (cx, cy)

    def dessiner(self, surface: pygame.Surface, etat: str, survol: bool):
        """Dessine le bouton avec la couleur et le label correspondant a l'etat."""
        couleur = (55, 85, 140) if survol else (35, 58, 105)
        rect_arrondi(surface, couleur, self.rect, rayon=8)

        if etat == "gagne":
            label, coul = " WIN!", T.COULEUR_SUCCES
        elif etat == "perdu":
            label, coul = " RIP!", T.COULEUR_ACCENT
        else:
            label, coul = "RESET", T.COULEUR_TEXTE

        texte_centre(surface, self._font, label, coul, self.rect)

    def collide(self, pos) -> bool:
        """Retourne True si la position donnee est dans le bouton."""
        return self.rect.collidepoint(pos)
