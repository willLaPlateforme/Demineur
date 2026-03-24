"""
GrilleRenderer : calcule les positions des cases et gère le rendu de la grille.
Fournit aussi la détection de case sous le curseur.
"""
import pygame
from plateau import Plateau
from graphique.case_renderer import CaseRenderer
from graphique.theme import TAILLE_CASE, GAP, MARGE_GRILLE, FOND_GRILLE
from graphique.dessin import rect_arrondi


class GrilleRenderer:
    """
    Gère le rendu complet de la grille et la conversion pixel ↔ case.
    """

    def __init__(self, plateau: Plateau, case_renderer: CaseRenderer,
                 offset_x: int, offset_y: int):
        self.plateau = plateau
        self._renderer = case_renderer
        self.offset_x = offset_x
        self.offset_y = offset_y
        self._mine_touchee: tuple[int, int] | None = None  # case qui a explosé

    def definir_mine_touchee(self, ligne: int, colonne: int):
        self._mine_touchee = (ligne, colonne)

    def reinitialiser(self, plateau: Plateau):
        self.plateau = plateau
        self._mine_touchee = None

    def largeur(self) -> int:
        return self.plateau.colonnes * (TAILLE_CASE + GAP) - GAP + 2 * MARGE_GRILLE

    def hauteur(self) -> int:
        return self.plateau.lignes * (TAILLE_CASE + GAP) - GAP + 2 * MARGE_GRILLE

    def rect_case(self, ligne: int, colonne: int) -> pygame.Rect:
        """Retourne le Rect pygame d'une case donnée."""
        x = self.offset_x + MARGE_GRILLE + colonne * (TAILLE_CASE + GAP)
        y = self.offset_y + MARGE_GRILLE + ligne * (TAILLE_CASE + GAP)
        return pygame.Rect(x, y, TAILLE_CASE, TAILLE_CASE)

    def case_sous_curseur(self, mx: int, my: int):
        """
        Retourne (ligne, colonne) de la case sous le curseur, ou None.
        """
        for l in range(self.plateau.lignes):
            for c in range(self.plateau.colonnes):
                if self.rect_case(l, c).collidepoint(mx, my):
                    return (l, c)
        return None

    def dessiner(self, surface: pygame.Surface, survol: tuple[int, int] | None):
        """Dessine le fond de grille puis toutes les cases."""
        grille_rect = pygame.Rect(
            self.offset_x, self.offset_y,
            self.largeur(), self.hauteur()
        )
        rect_arrondi(surface, FOND_GRILLE, grille_rect, rayon=6)

        for l in range(self.plateau.lignes):
            for c in range(self.plateau.colonnes):
                case = self.plateau.grille[l][c]
                rect = self.rect_case(l, c)
                est_survol = survol == (l, c) and not case.est_revelee()
                est_mine_touchee = self._mine_touchee == (l, c)
                self._renderer.dessiner(surface, case, rect, est_survol, est_mine_touchee)
