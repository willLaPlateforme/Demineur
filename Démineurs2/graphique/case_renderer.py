"""
CaseRenderer : dessine une case individuelle sur une Surface pygame.
Adapte aux attributs de Cases (Case.py) :
  case.etat          -> "cachee" | "revelee" | "drapeau" | "question"
  case.est_une_bombe -> bool
  case.nombre_de_bombes_autour -> int
"""
import pygame
from graphique import theme as T
from graphique.dessin import rect_arrondi, texte_centre, case_relief


class CaseRenderer:
    """
    Dessine l'etat visuel d'une Cases sur la surface pygame fournie.
    Instance unique partagee pour toutes les cases de la grille.
    """

    def __init__(self, font_chiffre: pygame.font.Font, font_symbole: pygame.font.Font):
        self._font_chiffre = font_chiffre
        self._font_symbole = font_symbole

    def dessiner(self, surface: pygame.Surface, case,
                 rect: pygame.Rect, survol: bool = False, mine_touchee: bool = False):
        """Dispatch vers la bonne methode selon case.etat."""
        if case.etat == "revelee":
            if case.est_une_bombe:
                self._mine(surface, rect, mine_touchee)
            elif case.nombre_de_bombes_autour > 0:
                self._chiffre(surface, rect, case.nombre_de_bombes_autour)
            else:
                self._vide(surface, rect)
        elif case.etat == "drapeau":
            self._drapeau(surface, rect)
        elif case.etat == "question":
            self._interrogation(surface, rect)
        else:  # "cachee"
            self._cachee(surface, rect, survol)

    # ── Rendus visuels ────────────────────────────────────────────────────────

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
        # Corps de la bombe dessine en formes geometriques
        cx, cy = rect.center
        r = T.TAILLE_CASE // 3
        pygame.draw.circle(surface, (20, 20, 20), (cx, cy), r)
        pygame.draw.circle(surface, (80, 80, 80), (cx - r//3, cy - r//3), r//4)
        # Meche
        pygame.draw.line(surface, (80, 80, 80), (cx, cy - r), (cx + 4, cy - r - 5), 2)
        if touchee:
            # Eclats orange
            for dx, dy in [(-r-4, 0), (r+4, 0), (0, -r-4), (0, r+4)]:
                pygame.draw.circle(surface, (255, 160, 0), (cx + dx, cy + dy), 3)

    def _drapeau(self, surface, rect):
        case_relief(surface, rect, T.FOND_CASE_DRAPEAU, T.BORD_CASE_CLAIR, T.BORD_CASE_SOMBRE)
        # Mat vertical
        mx = rect.centerx - 3
        pygame.draw.line(surface, (210, 210, 210),
                         (mx, rect.top + 6), (mx, rect.bottom - 7), 2)
        # Triangle rouge (drapeau)
        pts = [(mx, rect.top + 6), (mx + 13, rect.top + 12), (mx, rect.top + 18)]
        pygame.draw.polygon(surface, T.COULEUR_ACCENT, pts)
        # Pied du mat
        pygame.draw.line(surface, (210, 210, 210),
                         (mx - 4, rect.bottom - 7), (mx + 6, rect.bottom - 7), 2)

    def _interrogation(self, surface, rect):
        case_relief(surface, rect, T.FOND_CASE_CACHEE, T.BORD_CASE_CLAIR, T.BORD_CASE_SOMBRE)
        texte_centre(surface, self._font_chiffre, "?", (243, 156, 18), rect)
