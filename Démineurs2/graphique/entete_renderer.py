"""
EnteteRenderer : dessine la barre d'en-tete (mines, timer, bouton reset).
Affiche les infos issues de Jeu : nb_bombes_restantes, temps_formate,
compter_drapeaux, compter_questions.
"""
import pygame
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_gauche, texte_droite, texte_centre


class BoutonReset:
    """Bouton RESET cliquable dans l'en-tete."""

    LARGEUR = 80
    HAUTEUR = 34

    def __init__(self, font: pygame.font.Font):
        self._font = font
        self.rect = pygame.Rect(0, 0, self.LARGEUR, self.HAUTEUR)

    def centrer(self, cx: int, cy: int):
        self.rect.center = (cx, cy)

    def dessiner(self, surface: pygame.Surface, etat: str, survol: bool):
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
        return self.rect.collidepoint(pos)


class EnteteRenderer:
    """
    Dessine la zone d'en-tete :
      - Bombes restantes (gauche)
      - Bouton RESET (centre)
      - Timer (droite)
      - Compteurs drapeaux / questions (sous les infos)
    """

    def __init__(self, font_grand: pygame.font.Font, font_petit: pygame.font.Font,
                 font_btn: pygame.font.Font, largeur: int, offset_y: int):
        self._font_grand = font_grand
        self._font_petit = font_petit
        self._largeur    = largeur
        self._offset_y   = offset_y
        self.bouton = BoutonReset(font_btn)

    def dessiner(self, surface: pygame.Surface,
                 mines_restantes: int, temps: str,
                 nb_drapeaux: int, nb_interrogations: int,
                 etat: str, survol_reset: bool):

        # Fond de l'entete
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
