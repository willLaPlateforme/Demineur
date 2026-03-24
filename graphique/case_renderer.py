"""
CaseRenderer : dessine une case individuelle sur une Surface pygame.
Séparé de la logique de plateau pour respecter la responsabilité unique.
"""
import pygame
from case import Case
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_centre, case_relief


class CaseRenderer:
    """
    Dessine l'état visuel d'une Case sur la surface pygame fournie.
    Instancié une seule fois par GrilleRenderer, partagé pour toutes les cases.
    """

    def __init__(self, font_chiffre: pygame.font.Font, font_symbole: pygame.font.Font):
        self._font_chiffre = font_chiffre
        self._font_symbole = font_symbole

    def dessiner(self, surface: pygame.Surface, case: Case,
                 rect: pygame.Rect, survol: bool = False, mine_touchee: bool = False):
        """Dispatch vers la bonne méthode selon l'état de la case."""
        if case.est_revelee():
            if case.est_mine:
                self._mine(surface, rect, mine_touchee)
            elif case.mines_adjacentes > 0:
                self._chiffre(surface, rect, case.mines_adjacentes)
            else:
                self._vide(surface, rect)
        elif case.est_drapeautee():
            self._drapeau(surface, rect)
        elif case.est_interrogation():
            self._interrogation(surface, rect)
        else:
            self._cachee(surface, rect, survol)

    # ── États visuels ─────────────────────────────────────────────────────────

    def _cachee(self, surface, rect, survol):
        fond = T.FOND_CASE_SURVOL if survol else T.FOND_CASE_CACHEE
        case_relief(surface, rect, fond, T.BORD_CASE_CLAIR, T.BORD_CASE_SOMBRE)

    def _vide(self, surface, rect):
        rect_arrondi(surface, T.FOND_CASE_REVELEE, rect)
        pygame.draw.rect(surface, T.BORD_REVELEE, rect, 1, border_radius=T.RAYON)

    def _chiffre(self, surface, rect, n: int):
        rect_arrondi(surface, T.FOND_CASE_REVELEE, rect)
        pygame.draw.rect(surface, T.BORD_REVELEE, rect, 1, border_radius=T.RAYON)
        couleur = T.COULEURS_CHIFFRES.get(n, (50, 50, 50))
        texte_centre(surface, self._font_chiffre, str(n), couleur, rect)

    def _mine(self, surface, rect, touchee: bool):
        fond = T.FOND_CASE_MINE_HIT if touchee else T.FOND_CASE_MINE
        rect_arrondi(surface, fond, rect)
        texte_centre(surface, self._font_symbole, "💣", (255, 255, 255), rect)

    def _drapeau(self, surface, rect):
        case_relief(surface, rect, T.FOND_CASE_DRAPEAU, T.BORD_CASE_CLAIR, T.BORD_CASE_SOMBRE)
        texte_centre(surface, self._font_symbole, "🚩", T.COULEUR_ACCENT, rect)

    def _interrogation(self, surface, rect):
        case_relief(surface, rect, T.FOND_CASE_CACHEE, T.BORD_CASE_CLAIR, T.BORD_CASE_SOMBRE)
        couleur = (243, 156, 18)
        texte_centre(surface, self._font_chiffre, "?", couleur, rect)
