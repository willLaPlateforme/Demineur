"""
Utilitaires de dessin pygame : rectangles arrondis, texte centré, reliefs.
"""
import pygame
from graphique.theme import RAYON


def rect_arrondi(surface, couleur, rect, rayon=RAYON):
    pygame.draw.rect(surface, couleur, rect, border_radius=rayon)


def rect_arrondi_bord(surface, couleur, rect, epaisseur=1, rayon=RAYON):
    pygame.draw.rect(surface, couleur, rect, width=epaisseur, border_radius=rayon)


def texte_centre(surface, font, texte, couleur, rect):
    img = font.render(texte, True, couleur)
    r = img.get_rect(center=rect.center)
    surface.blit(img, r)


def texte_gauche(surface, font, texte, couleur, pos):
    img = font.render(texte, True, couleur)
    surface.blit(img, pos)


def texte_droite(surface, font, texte, couleur, pos_droite):
    img = font.render(texte, True, couleur)
    r = img.get_rect()
    r.right = pos_droite[0]
    r.y = pos_droite[1]
    surface.blit(img, r)


def case_relief(surface, rect, couleur_fond, couleur_clair, couleur_sombre):
    rect_arrondi(surface, couleur_fond, rect)
    pygame.draw.line(surface, couleur_clair, rect.topleft, rect.topright, 2)
    pygame.draw.line(surface, couleur_clair, rect.topleft, rect.bottomleft, 2)
    pygame.draw.line(surface, couleur_sombre,
                     (rect.right - 1, rect.top), rect.bottomright, 2)
    pygame.draw.line(surface, couleur_sombre,
                     (rect.left, rect.bottom - 1), rect.bottomright, 2)
