"""
BoutonBonus : bouton de la barre de bonus.
Affiche le nombre d'utilisations restantes et change d'apparence selon l'etat.
Une classe = un fichier (principe de responsabilite unique).
"""
import pygame
from graphique.dessin import rect_arrondi, texte_centre


class BoutonBonus:
    """
    Bouton de bonus : pose un drapeau automatique sur une bombe au hasard.
    Affiche le nombre d'utilisations restantes (max 3 par partie).
    Change de couleur selon l'etat (actif / epuise / partie non commencee).
    """

    LARGEUR = 260
    HAUTEUR = 36

    def __init__(self, font: pygame.font.Font):
        self._font = font
        self.rect  = pygame.Rect(0, 0, self.LARGEUR, self.HAUTEUR)

    def centrer(self, cx: int, cy: int):
        """Centre le bouton sur le point (cx, cy)."""
        self.rect.center = (cx, cy)

    def dessiner(self, surface: pygame.Surface, restants: int,
                 actif: bool, survol: bool):
        """
        Dessine le bouton selon son etat.
          restants : nombre d'utilisations restantes (0 a 3)
          actif    : True si la partie est en cours ET restants > 0
          survol   : True si la souris est dessus
        """
        if actif:
            fond  = (35, 130, 200) if not survol else (55, 155, 225)
            coul  = (255, 255, 255)
            label = f"DRAPEAU AUTO  ({restants} restant{'s' if restants > 1 else ''})"
        else:
            fond  = (195, 200, 210)
            coul  = (130, 135, 145)
            if restants == 0:
                label = "DRAPEAU AUTO  (epuise)"
            else:
                label = "DRAPEAU AUTO  (demarrez d'abord)"

        rect_arrondi(surface, fond, self.rect, rayon=9)

        if actif:
            pygame.draw.rect(surface, (255, 255, 255),
                             self.rect, 1, border_radius=9)

        texte_centre(surface, self._font, label, coul, self.rect)

        # Petits indicateurs visuels des 3 charges (cercles)
        r          = 5
        espacement = 14
        total      = 3 * (r * 2) + 2 * espacement
        start_x    = self.rect.centerx - total // 2 + r
        cy_ind     = self.rect.bottom + 8
        for i in range(3):
            cx_ind   = start_x + i * (r * 2 + espacement)
            coul_ind = (35, 130, 200) if i < restants else (200, 205, 215)
            pygame.draw.circle(surface, coul_ind, (cx_ind, cy_ind), r)

    def collide(self, pos) -> bool:
        """Retourne True si la position donnee est dans le bouton."""
        return self.rect.collidepoint(pos)
