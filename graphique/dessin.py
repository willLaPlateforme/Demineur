"""
Utilitaires de dessin pygame : rectangles arrondis, texte centré, reliefs.
"""
import pygame
from graphique.theme import RAYON


def rect_arrondi(surface: pygame.Surface, couleur, rect: pygame.Rect, rayon: int = RAYON):
    """Dessine un rectangle avec coins arrondis."""
    pygame.draw.rect(surface, couleur, rect, border_radius=rayon)


def rect_arrondi_bord(surface: pygame.Surface, couleur, rect: pygame.Rect,
                      epaisseur: int = 1, rayon: int = RAYON):
    """Dessine le contour d'un rectangle arrondi."""
    pygame.draw.rect(surface, couleur, rect, width=epaisseur, border_radius=rayon)


def texte_centre(surface: pygame.Surface, font: pygame.font.Font,
                 texte: str, couleur, rect: pygame.Rect):
    """Dessine du texte centré dans un rect."""
    img = font.render(texte, True, couleur)
    r = img.get_rect(center=rect.center)
    surface.blit(img, r)


def texte_gauche(surface: pygame.Surface, font: pygame.font.Font,
                 texte: str, couleur, pos: tuple):
    """Dessine du texte aligné à gauche depuis pos."""
    img = font.render(texte, True, couleur)
    surface.blit(img, pos)


def texte_droite(surface: pygame.Surface, font: pygame.font.Font,
                 texte: str, couleur, pos_droite: tuple):
    """Dessine du texte aligné à droite, pos_droite = (x_droite, y)."""
    img = font.render(texte, True, couleur)
    r = img.get_rect()
    r.right = pos_droite[0]
    r.y = pos_droite[1]
    surface.blit(img, r)


def case_relief(surface: pygame.Surface, rect: pygame.Rect,
                couleur_fond, couleur_clair, couleur_sombre):
    """
    Dessine une case avec un effet de relief 3D (style Windows 3.1 Minesweeper).
    """
    rect_arrondi(surface, couleur_fond, rect)
    # Bord clair en haut/gauche
    pygame.draw.line(surface, couleur_clair, rect.topleft, rect.topright, 2)
    pygame.draw.line(surface, couleur_clair, rect.topleft, rect.bottomleft, 2)
    # Bord sombre en bas/droite
    pygame.draw.line(surface, couleur_sombre,
                     (rect.right - 1, rect.top), rect.bottomright, 2)
    pygame.draw.line(surface, couleur_sombre,
                     (rect.left, rect.bottom - 1), rect.bottomright, 2)
