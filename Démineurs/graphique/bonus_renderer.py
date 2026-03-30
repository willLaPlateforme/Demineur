"""
BonusRenderer : barre de bonus avec deux boutons independants.
  - Bonus REVELER  : devoile une bombe cachee au hasard (visuellement, sans game over)
  - Bonus DRAPEAU  : pose un drapeau automatiquement sur une bombe cachee au hasard
Chaque bonus est utilisable une seule fois par partie.
"""
import pygame
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_centre, texte_gauche


class BoutonBonus:
    """
    Bouton generique pour un bonus.
    Vert et cliquable si actif, grise si deja utilise ou partie non demarree.
    """

    LARGEUR = 200
    HAUTEUR = 38

    def __init__(self, label_actif: str, label_utilise: str,
                 couleur_fond, couleur_survol, font: pygame.font.Font):
        self._label_actif   = label_actif
        self._label_utilise = label_utilise
        self._couleur_fond  = couleur_fond
        self._couleur_survol = couleur_survol
        self._font = font
        self.rect  = pygame.Rect(0, 0, self.LARGEUR, self.HAUTEUR)

    def placer(self, x: int, y: int):
        self.rect.topleft = (x, y)

    def dessiner(self, surface: pygame.Surface, actif: bool, survol: bool):
        if actif:
            fond  = self._couleur_survol if survol else self._couleur_fond
            coul  = (255, 255, 255)
            label = self._label_actif
            # Liseré doré
            rect_arrondi(surface, fond, self.rect, rayon=9)
            pygame.draw.rect(surface, T.COULEUR_BONUS_BORD,
                             self.rect, 2, border_radius=9)
        else:
            fond  = T.COULEUR_BONUS_UTILISE
            coul  = (155, 160, 170)
            label = self._label_utilise
            rect_arrondi(surface, fond, self.rect, rayon=9)

        texte_centre(surface, self._font, label, coul, self.rect)

    def collide(self, pos) -> bool:
        return self.rect.collidepoint(pos)


class BonusRenderer:
    """
    Barre de bonus entre l'en-tete et la grille.
    Contient deux boutons independants, chacun utilisable une fois par partie.
    """

    ESPACEMENT = 20   # espace entre les deux boutons

    def __init__(self, font_btn: pygame.font.Font, font_label: pygame.font.Font,
                 largeur: int, offset_y: int):
        self._font_btn   = font_btn
        self._font_label = font_label
        self._largeur    = largeur
        self._offset_y   = offset_y

        # Bonus 1 : reveler une bombe
        self.bouton_reveler = BoutonBonus(
            label_actif   = "VOIR une bombe  (x1)",
            label_utilise = "VOIR : utilise",
            couleur_fond  = (200, 80, 40),    # rouge-orange (bombe)
            couleur_survol = (225, 100, 55),
            font          = font_btn,
        )

        # Bonus 2 : poser un drapeau sur une bombe
        self.bouton_drapeau = BoutonBonus(
            label_actif   = "DRAPEAU auto  (x1)",
            label_utilise = "DRAPEAU : utilise",
            couleur_fond  = (40, 110, 200),   # bleu
            couleur_survol = (60, 135, 230),
            font          = font_btn,
        )

        self._positionner()

    def _positionner(self):
        """Centre les deux boutons horizontalement dans la barre."""
        total = BoutonBonus.LARGEUR * 2 + self.ESPACEMENT
        start_x = (self._largeur - total) // 2
        cy = self._offset_y + T.HAUTEUR_BONUS // 2 - BoutonBonus.HAUTEUR // 2
        self.bouton_reveler.placer(start_x, cy)
        self.bouton_drapeau.placer(start_x + BoutonBonus.LARGEUR + self.ESPACEMENT, cy)

    def mettre_a_jour_largeur(self, largeur: int):
        self._largeur = largeur
        self._positionner()

    def dessiner(self, surface: pygame.Surface,
                 reveler_dispo: bool, drapeau_dispo: bool,
                 survol_pos, etat_jeu: str):
        """Dessine la barre et les deux boutons."""

        # Fond jaune pale de la barre
        rect_arrondi(surface, T.COULEUR_BONUS_FOND,
                     pygame.Rect(0, self._offset_y, self._largeur, T.HAUTEUR_BONUS),
                     rayon=0)

        # Bords
        pygame.draw.rect(surface, T.COULEUR_BONUS_BORD,
                         (0, self._offset_y, self._largeur, 1))
        pygame.draw.rect(surface, T.COULEUR_BONUS_BORD,
                         (0, self._offset_y + T.HAUTEUR_BONUS - 1, self._largeur, 1))

        # Les boutons ne sont cliquables que si la partie est en cours
        en_cours = etat_jeu == "en_cours"

        actif_rev = reveler_dispo and en_cours
        actif_dra = drapeau_dispo and en_cours

        survol_rev = actif_rev and self.bouton_reveler.collide(survol_pos)
        survol_dra = actif_dra and self.bouton_drapeau.collide(survol_pos)

        self.bouton_reveler.dessiner(surface, actif_rev, survol_rev)
        self.bouton_drapeau.dessiner(surface, actif_dra, survol_dra)
