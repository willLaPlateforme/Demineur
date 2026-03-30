"""
EnteteRenderer : dessine la barre d'en-tete (mines, timer, bouton reset).
Importe BoutonReset depuis bouton_reset.py (une classe par fichier).
"""
import pygame
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_gauche, texte_droite
from graphique.bouton_reset import BoutonReset


class EnteteRenderer:
    """
    Dessine la zone d'en-tete :
      - Bombes restantes (gauche)
      - Bouton RESET (centre) -- importe depuis bouton_reset.py
      - Timer (droite)
      - Compteurs drapeaux / questions (sous les infos)
    """

    def __init__(self, font_grand: pygame.font.Font, font_petit: pygame.font.Font,
                 font_btn: pygame.font.Font, largeur: int, offset_y: int):
        self._font_grand = font_grand
        self._font_petit = font_petit
        self._largeur    = largeur
        self._offset_y   = offset_y
        self.bouton = BoutonReset(font_btn)   # une instance de BoutonReset

    def dessiner(self, surface: pygame.Surface,
                 mines_restantes: int, temps: str,
                 nb_drapeaux: int, nb_interrogations: int,
                 etat: str, survol_reset: bool):

        # Fond de l'en-tete
        rect_fond = pygame.Rect(0, self._offset_y, self._largeur, T.HAUTEUR_ENTETE)
        rect_arrondi(surface, T.FOND_ENTETE, rect_fond, rayon=0)

        cy = self._offset_y + T.HAUTEUR_ENTETE // 2

        # Bouton RESET centre
        self.bouton.centrer(self._largeur // 2, cy)
        self.bouton.dessiner(surface, etat, survol_reset)

        # Bombes restantes (gauche)
        texte_gauche(surface, self._font_grand,
                     f"BOMBES: {max(mines_restantes, 0):03d}",
                     T.COULEUR_ACCENT,
                     (14, self._offset_y + 10))

        texte_gauche(surface, self._font_petit,
                     f"F:{nb_drapeaux}  ?:{nb_interrogations}",
                     T.COULEUR_TEXTE,
                     (14, self._offset_y + 42))

        # Timer (droite)
        texte_droite(surface, self._font_grand,
                     f"TEMPS: {temps}",
                     T.COULEUR_ACCENT,
                     (self._largeur - 14, self._offset_y + 10))
