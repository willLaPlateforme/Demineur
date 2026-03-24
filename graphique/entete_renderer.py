"""
EnteteRenderer : dessine la barre d'en-tête (mines, timer, bouton reset).
"""
import pygame
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_gauche, texte_droite, texte_centre


class BoutonReset:
    """Bouton smiley cliquable dans l'en-tête."""

    TAILLE = 44

    def __init__(self, font: pygame.font.Font):
        self._font = font
        self.rect = pygame.Rect(0, 0, self.TAILLE, self.TAILLE)

    def centrer(self, cx: int, cy: int):
        self.rect.center = (cx, cy)

    def dessiner(self, surface: pygame.Surface, emoji: str, survol: bool):
        couleur = (55, 85, 140) if survol else (35, 58, 105)
        rect_arrondi(surface, couleur, self.rect, rayon=22)
        texte_centre(surface, self._font, emoji, T.COULEUR_TEXTE, self.rect)

    def collide(self, pos) -> bool:
        return self.rect.collidepoint(pos)


class EnteteRenderer:
    """
    Dessine la zone d'en-tête du jeu :
      - Mines restantes (gauche)
      - Bouton reset smiley (centre)
      - Timer (droite)
      - Drapeaux / interrogations (sous les infos)
    """

    def __init__(self, font_grand: pygame.font.Font, font_petit: pygame.font.Font,
                 font_emoji: pygame.font.Font, largeur: int, offset_y: int):
        self._font_grand = font_grand
        self._font_petit = font_petit
        self._font_emoji = font_emoji
        self._largeur = largeur
        self._offset_y = offset_y
        self.bouton = BoutonReset(font_emoji)

    def dessiner(self, surface: pygame.Surface,
                 mines_restantes: int, temps: str,
                 nb_drapeaux: int, nb_interrogations: int,
                 etat: str, survol_reset: bool):
        # Fond
        rect_fond = pygame.Rect(0, self._offset_y, self._largeur, T.HAUTEUR_ENTETE)
        rect_arrondi(surface, T.FOND_ENTETE, rect_fond, rayon=0)

        cy = self._offset_y + T.HAUTEUR_ENTETE // 2

        # Bouton reset centré
        self.bouton.centrer(self._largeur // 2, cy)
        if etat == "gagne":
            emoji = "😎"
        elif etat == "perdu":
            emoji = "😵"
        else:
            emoji = "🙂"
        self.bouton.dessiner(surface, emoji, survol_reset)

        # Mines restantes (gauche)
        texte_mines = f"💣 {max(mines_restantes, 0):03d}"
        texte_gauche(surface, self._font_grand, texte_mines, T.COULEUR_ACCENT,
                     (14, self._offset_y + 10))
        marqueurs = f"🚩{nb_drapeaux}  ❓{nb_interrogations}"
        texte_gauche(surface, self._font_petit, marqueurs, T.COULEUR_TEXTE,
                     (14, self._offset_y + 42))

        # Timer (droite)
        texte_timer = f"⏱ {temps}"
        texte_droite(surface, self._font_grand, texte_timer, T.COULEUR_ACCENT,
                     (self._largeur - 14, self._offset_y + 10))
